import sys
import random


def get_key_from_seed(seed, n):
    random.seed(seed)
    return random.randbytes(n)


def main():
    if len(sys.argv) < 4:
        return

    key_size = int(sys.argv[1])
    crypt_file = sys.argv[2]
    target_words = [w.encode() for w in sys.argv[3:]]

    with open(crypt_file, "rb") as f:
        ciphertext = f.read()

    for i in range(65536):
        seed = i.to_bytes(2, "big")
        candidate_key = get_key_from_seed(seed, key_size)

        plaintext = bytes([c ^ k for c, k in zip(ciphertext, candidate_key)])

        if any(word in plaintext for word in target_words):
            print(plaintext.decode(errors="ignore").strip())
            break


if __name__ == "__main__":
    main()
