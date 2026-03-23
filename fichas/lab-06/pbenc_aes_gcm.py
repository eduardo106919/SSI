import sys
import os
import getpass
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
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
    password = getpass.getpass("Introduza a pass-phrase para cifrar (GCM): ")

    with open(file_path, "rb") as f:
        plaintext = f.read()

    salt = os.urandom(16)
    nonce = os.urandom(12)

    key = derive_key(password, salt)
    aesgcm = AESGCM(key)

    ciphertext = aesgcm.encrypt(nonce, plaintext, None)

    with open(file_path + ".enc", "wb") as f:
        f.write(salt + nonce + ciphertext)
    print(f"Ficheiro cifrado com AES-GCM: {file_path}.enc")


def dec(file_path):
    password = getpass.getpass("Introduza a pass-phrase para decifrar (GCM): ")

    with open(file_path, "rb") as f:
        salt = f.read(16)
        nonce = f.read(12)
        ciphertext = f.read()

    key = derive_key(password, salt)
    aesgcm = AESGCM(key)

    try:
        plaintext = aesgcm.decrypt(nonce, ciphertext, None)

        with open(file_path + ".dec", "wb") as f:
            f.write(plaintext)
        print(f"Ficheiro decifrado com sucesso: {file_path}.dec")
    except Exception:
        print("Erro: Falha na autenticação ou password incorreta.")
        sys.exit(1)


def main():
    if len(sys.argv) < 3:
        print("Usage: python pbenc_aes_gcm.py <enc|dec> <ficheiro>")
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
