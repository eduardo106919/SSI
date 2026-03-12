import sys
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


def setup(key_file):
    key = os.urandom(32)
    with open(key_file, "wb") as f:
        f.write(key)
    print(f"Chave gerada e guardada em: {key_file}")


def enc(file_path, key_file):
    with open(key_file, "rb") as f:
        key = f.read()

    with open(file_path, "rb") as f:
        plaintext = f.read()

    nonce = os.urandom(16)
    algorithm = algorithms.ChaCha20(key, nonce)
    cipher = Cipher(algorithm, mode=None)
    encryptor = cipher.encryptor()

    ciphertext = encryptor.update(plaintext)

    with open(file_path + ".enc", "wb") as f:
        f.write(nonce + ciphertext)
    print(f"Ficheiro cifrado: {file_path}.enc")


def dec(file_path, key_file):
    with open(key_file, "rb") as f:
        key = f.read()

    with open(file_path, "rb") as f:
        nonce = f.read(16)
        ciphertext = f.read()

    algorithm = algorithms.ChaCha20(key, nonce)
    cipher = Cipher(algorithm, mode=None)
    decryptor = cipher.decryptor()

    plaintext = decryptor.update(ciphertext)

    with open(file_path + ".dec", "wb") as f:
        f.write(plaintext)
    print(f"Ficheiro decifrado: {file_path}.dec")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python cfich_chacha20.py <setup|enc|dec> <args...>")
        sys.exit(1)

    op = sys.argv[1]

    if op == "setup":
        setup(sys.argv[2])
    elif op == "enc":
        enc(sys.argv[2], sys.argv[3])
    elif op == "dec":
        dec(sys.argv[2], sys.argv[3])
    else:
        print("Operação inválida.")
