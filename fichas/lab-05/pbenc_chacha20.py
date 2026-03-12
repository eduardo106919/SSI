import sys
import os
import getpass
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend


def derive_key(password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend(),
    )
    return kdf.derive(password.encode())


def enc(file_path):
    password = getpass.getpass("Introduza a pass-phrase para cifrar: ")

    with open(file_path, "rb") as f:
        plaintext = f.read()

    salt = os.urandom(16)
    nonce = os.urandom(16)

    key = derive_key(password, salt)

    algorithm = algorithms.ChaCha20(key, nonce)
    cipher = Cipher(algorithm, mode=None)
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext)

    with open(file_path + ".enc", "wb") as f:
        f.write(salt + nonce + ciphertext)
    print(f"Ficheiro cifrado com sucesso: {file_path}.enc")


def dec(file_path):
    password = getpass.getpass("Introduza a pass-phrase para decifrar: ")

    with open(file_path, "rb") as f:
        salt = f.read(16)
        nonce = f.read(16)
        ciphertext = f.read()

    key = derive_key(password, salt)

    algorithm = algorithms.ChaCha20(key, nonce)
    cipher = Cipher(algorithm, mode=None)
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(ciphertext)

    with open(file_path + ".dec", "wb") as f:
        f.write(plaintext)
    print(f"Ficheiro decifrado com sucesso: {file_path}.dec")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python pbenc_chacha20.py <enc|dec> <ficheiro>")
        sys.exit(1)

    op = sys.argv[1]
    path = sys.argv[2]

    if op == "enc":
        enc(path)
    elif op == "dec":
        dec(path)
    else:
        print("Operação inválida.")
