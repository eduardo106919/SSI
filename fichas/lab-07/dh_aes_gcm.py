import os
from multiprocessing import Process, Pipe

from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives.serialization import (
    Encoding,
    PublicFormat,
    load_der_public_key,
)
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


p = 0xD482E32A0DE0B2E4FB9FFA7BEB9F090BA310ED56A75A07D49FBE1551B3071E9A561486E7D5A5B41D4F3C879887F15B181337467EEAF61E753BF06258F6117D77
g = 2

params = dh.DHParameterNumbers(p, g).parameters()


def derive_aes_key(shared_secret: bytes) -> bytes:
    return HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b"dh_aes_gcm",
    ).derive(shared_secret)


def alice_process(conn):
    # DH key exchange
    alice_private = params.generate_private_key()
    alice_public = alice_private.public_key()

    # send Alice's public key to Bob
    alice_bytes = alice_public.public_bytes(
        Encoding.DER, PublicFormat.SubjectPublicKeyInfo
    )
    conn.send(alice_bytes)

    # receive Bob's public key
    bob_bytes = conn.recv()
    bob_public = load_der_public_key(bob_bytes)

    # compare shared secret K and derive AES key
    K = alice_private.exchange(bob_public)
    aes_key = derive_aes_key(K)
    print(f"[Alice] K       = {K.hex()}")
    print(f"[Alice] aes_key = {aes_key.hex()}")

    plaintext = b"Hello Bob, this message is confidential!"

    nonce = os.urandom(12)
    aesgcm = AESGCM(aes_key)
    ciphertext = aesgcm.encrypt(nonce, plaintext, None)

    # send (nonce + ciphertext) to Bob
    conn.send(nonce + ciphertext)
    print(f"[Alice] Sent encrypted message (nonce={nonce.hex()})")


def bob_process(conn):
    # DH key exchange
    bob_private = params.generate_private_key()
    bob_public = bob_private.public_key()

    # receive Alice's public key
    alice_bytes = conn.recv()
    alice_public = load_der_public_key(alice_bytes)

    # send Bob's public key to Alice
    bob_bytes = bob_public.public_bytes(Encoding.DER, PublicFormat.SubjectPublicKeyInfo)
    conn.send(bob_bytes)

    # compare shared secret K and derive AES key
    K = bob_private.exchange(alice_public)
    aes_key = derive_aes_key(K)
    print(f"[Bob]   K       = {K.hex()}")
    print(f"[Bob]   aes_key = {aes_key.hex()}")

    # receive (nonce + ciphertext)
    message = conn.recv()
    nonce = message[:12]
    ciphertext = message[12:]

    aesgcm = AESGCM(aes_key)
    plaintext = aesgcm.decrypt(nonce, ciphertext, None)
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
