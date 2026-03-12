import sys


def attack(fctxt, pos, ptxt_at_pos, new_ptxt_at_pos):
    pos = int(pos)
    old_bytes = ptxt_at_pos.encode("utf-8")
    new_bytes = new_ptxt_at_pos.encode("utf-8")

    if len(old_bytes) != len(new_bytes):
        print("Erro: O fragmento original e o novo devem ter o mesmo tamanho.")
        sys.exit(1)

    with open(fctxt, "rb") as f:
        ciphertext = bytearray(f.read())

    actual_pos = 16 + pos

    if actual_pos + len(old_bytes) > len(ciphertext):
        print("Erro: Posição ou tamanho fora dos limites do ficheiro.")
        sys.exit(1)

    for i in range(len(old_bytes)):
        ciphertext[actual_pos + i] = (
            ciphertext[actual_pos + i] ^ old_bytes[i] ^ new_bytes[i]
        )

    output_filename = fctxt + ".attck"
    with open(output_filename, "wb") as f:
        f.write(ciphertext)

    print(f"Ataque concluído. Ficheiro gravado em: {output_filename}")


if __name__ == "__main__":
    if len(sys.argv) != 5:
        print(
            "Usage: python chacha20_int_attck.py <fctxt> <pos> <ptxtAtPos> <newPtxtAtPos>"
        )
        sys.exit(1)

    attack(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
