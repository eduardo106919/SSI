import sys
import os
import getpass
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes, hmac
from cryptography.hazmat.backends import default_backend


def derive_keys(password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=64,
        salt=salt,
        iterations=100000,
        backend=default_backend(),
    )
    keys = kdf.derive(password.encode())
    return keys[:32], keys[32:]


def enc(file_path):
    password = getpass.getpass("Introduza a pass-phrase para cifrar: ")

    with open(file_path, "rb") as f:
        plaintext = f.read()

    salt = os.urandom(16)
    nonce = os.urandom(16)

    enc_key, mac_key = derive_keys(password, salt)

    algorithm = algorithms.AES(enc_key)
    cipher = Cipher(algorithm, modes.CTR(nonce), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()

    h = hmac.HMAC(mac_key, hashes.SHA256(), backend=default_backend())
    h.update(nonce + ciphertext)
    tag = h.finalize()

    with open(file_path + ".enc", "wb") as f:
        f.write(salt + nonce + tag + ciphertext)
    print(f"Ficheiro cifrado e autenticado: {file_path}.enc")


def dec(file_path):
    password = getpass.getpass("Introduza a pass-phrase para decifrar: ")

    with open(file_path, "rb") as f:
        salt = f.read(16)
        nonce = f.read(16)
        tag = f.read(32)
        ciphertext = f.read()

    enc_key, mac_key = derive_keys(password, salt)

    h = hmac.HMAC(mac_key, hashes.SHA256(), backend=default_backend())
    h.update(nonce + ciphertext)
    try:
        h.verify(tag)
    except Exception:
        print("Erro: Falha na verificação de integridade (MAC inválido).")
        sys.exit(1)

    algorithm = algorithms.AES(enc_key)
    cipher = Cipher(algorithm, modes.CTR(nonce), backend=default_backend())
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()

    with open(file_path + ".dec", "wb") as f:
        f.write(plaintext)
    print(f"Ficheiro decifrado com sucesso: {file_path}.dec")


def main():
    if len(sys.argv) < 3:
        print("Usage: python pbenc_aes_ctr_hmac.py <enc|dec> <ficheiro>")
        sys.exit(1)

    op = sys.argv[1]
    path = sys.argv[2]

    if op == "enc":
        enc(path)
    elif op == "dec":
        dec(path)
    else:
        print("Operação inválida.")


if __name__ == "__main__":
    main()
