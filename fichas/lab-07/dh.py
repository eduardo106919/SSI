from multiprocessing import Process, Pipe
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives.serialization import (
    Encoding,
    PublicFormat,
    load_der_public_key,
)


p = 0xD482E32A0DE0B2E4FB9FFA7BEB9F090BA310ED56A75A07D49FBE1551B3071E9A561486E7D5A5B41D4F3C879887F15B181337467EEAF61E753BF06258F6117D77
g = 2

params = dh.DHParameterNumbers(p, g).parameters()


def alice_process(conn):
    # generate Alice's private/public keys
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

    # compute shared secret K
    K = alice_private.exchange(bob_public)
    print(f"[Alice] K = {K.hex()}")


def bob_process(conn):
    # generate Bob's private/public keys
    bob_private = params.generate_private_key()
    bob_public = bob_private.public_key()

    # receive Alice's public key
    alice_bytes = conn.recv()
    alice_public = load_der_public_key(alice_bytes)

    # send Bob's public key to Alice
    bob_bytes = bob_public.public_bytes(Encoding.DER, PublicFormat.SubjectPublicKeyInfo)
    conn.send(bob_bytes)

    # compute shared secret K
    K = bob_private.exchange(alice_public)
    print(f"[Bob]   K = {K.hex()}")


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
