import sys


def preproc(text):
    return "".join(c.upper() for c in text if c.isalpha())


def get_offsets(key: str):
    return [(ord(c) - ord("A")) % 26 for c in key.upper()]


def vigenere_transform(key_offsets: list, msg: str, decrypt=False):
    out = []
    key_len = len(key_offsets)

    for i, char in enumerate(msg):
        shift = key_offsets[i % key_len]
        if decrypt:
            shift = -shift

        char_idx = ord(char) - ord("A")
        new_idx = (char_idx + shift) % 26
        out.append(chr(new_idx + ord("A")))

    return "".join(out)


def main():
    if len(sys.argv) != 4:
        print("usage: python vigenere.py <enc|dec> <key> <message>")
    else:
        op = sys.argv[1]
        key_str = sys.argv[2]
        message = preproc(sys.argv[3])

        offsets = get_offsets(key_str)

        if op == "enc":
            print(vigenere_transform(offsets, message, decrypt=False))
        elif op == "dec":
            print(vigenere_transform(offsets, message, decrypt=True))


if __name__ == "__main__":
    main()
