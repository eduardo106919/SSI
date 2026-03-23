import sys
import os
from cryptography.hazmat.primitives import hashes


def calculate_prefix_mac(key, data):
    digest = hashes.Hash(hashes.SHA256())
    digest.update(key)
    digest.update(data)
    return digest.finalize()


def setup(fkey):
    key = os.urandom(32)
    with open(fkey, "wb") as f:
        f.write(key)
    print(f"Chave gerada e guardada em: {fkey}")


def mac(fich, fkey):
    with open(fkey, "rb") as f:
        key = f.read()

    with open(fich, "rb") as f:
        data = f.read()

    mac_value = calculate_prefix_mac(key, data)

    mac_filename = fich + ".mac"
    with open(mac_filename, "wb") as f:
        f.write(mac_value)
    print(f"MAC gravado em: {mac_filename}")


def ver(fich, fkey):
    with open(fkey, "rb") as f:
        key = f.read()

    with open(fich, "rb") as f:
        data = f.read()

    mac_filename = fich + ".mac"
    if not os.path.exists(mac_filename):
        print("Erro: Ficheiro .mac não encontrado.")
        return

    with open(mac_filename, "rb") as f:
        stored_mac = f.read()

    current_mac = calculate_prefix_mac(key, data)

    is_valid = current_mac == stored_mac
    print(is_valid)


def main():
    if len(sys.argv) < 3:
        print("Usage: python mac_sha256.py [setup|mac|ver] <args...>")
        return

    op = sys.argv[1]

    if op == "setup":
        setup(sys.argv[2])
    elif op == "mac":
        if len(sys.argv) < 4:
            print("Usage: python mac_sha256.py mac <fich> <fkey>")
        else:
            mac(sys.argv[2], sys.argv[3])
    elif op == "ver":
        if len(sys.argv) < 4:
            print("Usage: python mac_sha256.py ver <fich> <fkey>")
        else:
            ver(sys.argv[2], sys.argv[3])
    else:
        print("Operação inválida.")


if __name__ == "__main__":
    main()
