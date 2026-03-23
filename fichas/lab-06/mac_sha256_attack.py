import sys
import hashpumpy


def run_attack(fich, ext):
    try:
        with open(fich, "rb") as f:
            original_data = f.read()
    except FileNotFoundError:
        print(f"Erro: Ficheiro {fich} não encontrado.")
        return

    mac_fich = fich + ".mac"
    try:
        with open(mac_fich, "rb") as f:
            original_mac_bytes = f.read()
            original_mac_hex = original_mac_bytes.hex()
    except FileNotFoundError:
        print(f"Erro: Ficheiro de MAC {mac_fich} não encontrado.")
        return

    key_len = 32

    new_mac_hex, extended_data = hashpumpy.hashpump(
        original_mac_hex, original_data, ext.encode("utf-8"), key_len
    )

    new_fich_name = fich + ".ext"
    with open(new_fich_name, "wb") as f:
        f.write(extended_data)

    new_mac_fich_name = new_fich_name + ".mac"
    with open(new_mac_fich_name, "wb") as f:
        f.write(bytes.fromhex(new_mac_hex))

    print(f"Ataque concluído com sucesso!")
    print(f"Nova mensagem gravada em: {new_fich_name}")
    print(f"Novo MAC forjado gravado em: {new_mac_fich_name}")


def main():
    if len(sys.argv) != 3:
        print("Usage: python mac_sha256_attack.py <fich> <ext>")
    else:
        run_attack(sys.argv[1], sys.argv[2])


if __name__ == "__main__":
    main()
