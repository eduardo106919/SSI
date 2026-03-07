import sys


def preproc(text):
    return "".join(c.upper() for c in text if c.isalpha())


def usage():
    print("usage: python cesar.py <op> <key> <message>")


def cesar_encrypt(key: int, msg: str):
    out = ""
    key = key % 26
    for c in msg:
        shifted = (ord(c) - ord("A") + key) % 26
        out += chr(shifted + ord("A"))

    return out


def cesar_decrypt(key: int, msg: str):
    return cesar_encrypt(-key, msg)


def main():
    if len(sys.argv) != 4:
        usage()
    else:
        if sys.argv[1] == "enc":
            out = cesar_encrypt(ord(sys.argv[2]) - ord("A"), preproc(sys.argv[3]))
        elif sys.argv[1] == "dec":
            out = cesar_decrypt(ord(sys.argv[2]) - ord("A"), preproc(sys.argv[3]))

        print(out)


if __name__ == "__main__":
    main()
