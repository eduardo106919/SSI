import sys
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding


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

    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(plaintext) + padder.finalize()

    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()

    with open(file_path + ".enc", "wb") as f:
        f.write(iv + ciphertext)
    print(f"Ficheiro cifrado: {file_path}.enc")


def dec(file_path, key_file):
    with open(key_file, "rb") as f:
        key = f.read()
    with open(file_path, "rb") as f:
        iv = f.read(16)
        ciphertext = f.read()

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()

    unpadder = padding.PKCS7(128).unpadder()
    plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()

    with open(file_path + ".dec", "wb") as f:
        f.write(plaintext)
    print(f"Ficheiro decifrado: {file_path}.dec")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python cfich_aes_cbc.py <setup|enc|dec> <file_path> <key_file>")
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
