import sys


def usage():
    print("usage: python cesar_attack.py <msg> <word ...>")


def decrypt(msg: str, key: int):
    out = ""
    for c in msg:
        if "A" <= c <= "Z":
            idx = (ord(c) - ord("A") - key) % 26
            out += chr(idx + ord("A"))
        else:
            out += c
    return out


def main():
    if len(sys.argv) < 3:
        usage()
    else:
        msg = sys.argv[1].upper()
        target_words = [w.upper() for w in sys.argv[2:]]

        for i in range(26):
            candidate = decrypt(msg, i)

            if any(word in candidate for word in target_words):
                key_char = chr(ord("A") + i)
                print(key_char)
                print(candidate)
                return


if __name__ == "__main__":
    main()
