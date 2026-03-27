import os
from multiprocessing import Process, Pipe

from cryptography.hazmat.primitives.asymmetric import dh, padding
from cryptography.hazmat.primitives.serialization import (
    Encoding,
    PublicFormat,
    load_der_public_key,
    load_pem_private_key,
)
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.x509 import load_pem_x509_certificate
from cryptography.exceptions import InvalidSignature


CA_CERT = "CA.crt"
ALICE_KEY = "Alice.key"
ALICE_CERT = "Alice.crt"
BOB_KEY = "Bob.key"
BOB_CERT = "Bob.crt"


p = 0xD482E32A0DE0B2E4FB9FFA7BEB9F090BA310ED56A75A07D49FBE1551B3071E9A561486E7D5A5B41D4F3C879887F15B181337467EEAF61E753BF06258F6117D77
g = 2

params = dh.DHParameterNumbers(p, g).parameters()


def derive_aes_key(shared_secret: bytes) -> bytes:
    return HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b"sts_aes_gcm",
    ).derive(shared_secret)


def mkpair(x: bytes, y: bytes) -> bytes:
    """Encode the pair (x, y) into a single byte-string."""
    len_x_bytes = len(x).to_bytes(2, "little")
    return len_x_bytes + x + y


def unpair(xy: bytes):
    """Decode a pair produced by mkpair."""
    len_x = int.from_bytes(xy[:2], "little")
    x = xy[2 : len_x + 2]
    y = xy[len_x + 2 :]
    return x, y


def sign(private_key, *parts: bytes) -> bytes:
    """Sign the concatenation of all parts with RSA-PSS."""
    message = b"".join(parts)
    return private_key.sign(
        message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH,
        ),
        hashes.SHA256(),
    )


def verify_signature(cert, signature: bytes, *parts: bytes):
    """Verify an RSA-PSS signature using the public key from a certificate."""
    message = b"".join(parts)
    cert.public_key().verify(
        signature,
        message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH,
        ),
        hashes.SHA256(),
    )


def verify_certificate(cert_bytes: bytes, ca_cert) -> object:
    """
    Load a PEM certificate and verify it was signed by the CA.
    Returns the certificate object if valid, raises otherwise.
    """
    cert = load_pem_x509_certificate(cert_bytes)
    ca_cert.public_key().verify(
        cert.signature,
        cert.tbs_certificate_bytes,
        padding.PKCS1v15(),
        cert.signature_hash_algorithm,
    )
    return cert


def alice_process(conn):
    # load Alice's RSA private key and certificate
    with open(ALICE_KEY, "rb") as f:
        alice_rsa = load_pem_private_key(f.read(), None)
    with open(ALICE_CERT, "rb") as f:
        alice_cert_bytes = f.read()
    with open(CA_CERT, "rb") as f:
        ca_cert = load_pem_x509_certificate(f.read())

    # generate Alice's DH key pair
    alice_dh_private = params.generate_private_key()
    alice_dh_public = alice_dh_private.public_key()
    alice_dh_bytes = alice_dh_public.public_bytes(
        Encoding.DER, PublicFormat.SubjectPublicKeyInfo
    )

    # send g^x to Bob
    conn.send(alice_dh_bytes)
    print("[Alice] Sent DH public key (g^x)")

    # receive g^y, SigB(g^y, g^x), CertB from Bob
    msg2 = conn.recv()
    bob_dh_bytes, rest = unpair(msg2)
    bob_sig, cert_bob_bytes = unpair(rest)

    # verify Bob's certificate against the CA
    bob_cert = verify_certificate(cert_bob_bytes, ca_cert)
    print("[Alice] Bob's certificate is valid")

    # verify Bob's signature over (g^y, g^x)
    verify_signature(bob_cert, bob_sig, bob_dh_bytes, alice_dh_bytes)
    print("[Alice] Bob's signature is valid")

    # send SigA(g^x, g^y), CertA to Bob
    alice_sig = sign(alice_rsa, alice_dh_bytes, bob_dh_bytes)
    msg3 = mkpair(alice_sig, alice_cert_bytes)
    conn.send(msg3)
    print("[Alice] Sent signature and certificate")

    # compute shared secret K and derive AES key
    bob_dh_public = load_der_public_key(bob_dh_bytes)
    K = alice_dh_private.exchange(bob_dh_public)
    aes_key = derive_aes_key(K)
    print(f"[Alice] K       = {K.hex()}")
    print(f"[Alice] aes_key = {aes_key.hex()}")

    # encrypt and send a message
    plaintext = b"Hello Bob, this is authenticated and confidential!"
    nonce = os.urandom(12)
    ciphertext = AESGCM(aes_key).encrypt(nonce, plaintext, None)
    conn.send(nonce + ciphertext)
    print(f"[Alice] Sent encrypted message (nonce={nonce.hex()})")


def bob_process(conn):
    # load Bob's RSA private key and certificate
    with open(BOB_KEY, "rb") as f:
        bob_rsa = load_pem_private_key(f.read(), None)
    with open(BOB_CERT, "rb") as f:
        bob_cert_bytes = f.read()
    with open(CA_CERT, "rb") as f:
        ca_cert = load_pem_x509_certificate(f.read())

    # generate Bob's DH key pair
    bob_dh_private = params.generate_private_key()
    bob_dh_public = bob_dh_private.public_key()
    bob_dh_bytes = bob_dh_public.public_bytes(
        Encoding.DER, PublicFormat.SubjectPublicKeyInfo
    )

    # send g^x to Bob
    alice_dh_bytes = conn.recv()
    print("[Bob]   Received Alice's DH public key (g^x)")

    # receive g^y, SigB(g^y, g^x), CertB from Alice
    bob_sig = sign(bob_rsa, bob_dh_bytes, alice_dh_bytes)
    msg2 = mkpair(bob_dh_bytes, mkpair(bob_sig, bob_cert_bytes))
    conn.send(msg2)
    print("[Bob]   Sent DH public key, signature and certificate")

    # send SigA(g^x, g^y), CertA to Bob
    msg3 = conn.recv()
    alice_sig, alice_cert_bytes = unpair(msg3)

    # verify Alice's certificate against the CA
    alice_cert = verify_certificate(alice_cert_bytes, ca_cert)
    print("[Bob]   Alice's certificate is valid")

    # verify Alice's signature over (g^x, g^y)
    verify_signature(alice_cert, alice_sig, alice_dh_bytes, bob_dh_bytes)
    print("[Bob]   Alice's signature is valid")

    # compute shared secret K and derive AES key
    alice_dh_public = load_der_public_key(alice_dh_bytes)
    K = bob_dh_private.exchange(alice_dh_public)
    aes_key = derive_aes_key(K)
    print(f"[Bob]   K       = {K.hex()}")
    print(f"[Bob]   aes_key = {aes_key.hex()}")

    # receive and decrypt Alice's message
    message = conn.recv()
    nonce = message[:12]
    ciphertext = message[12:]
    plaintext = AESGCM(aes_key).decrypt(nonce, ciphertext, None)
    print(f"[Bob]   Decrypted message: {plaintext.decode()}")


def main():
    parent_conn, child_conn = Pipe()
    p1 = Process(target=alice_process, args=(parent_conn,))
    p2 = Process(target=bob_process, args=(child_conn,))
    p1.start()
    p2.start()
    p1.join()
    p2.join()


if __name__ == "__main__":
    main()
