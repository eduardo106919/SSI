import sys
import string

# approximate Portuguese letter frequencies
PORTUGUESE_FREQ_ORDER = "AEOSRIDMUNTPCLVGHQBFZJXKWY"

ALPHABET = string.ascii_uppercase
ALPHABET_SIZE = 26


def caesar_decrypt(text, shift):
    result = []
    for c in text:
        if c in ALPHABET:
            idx = (ord(c) - ord("A") - shift) % 26
            result.append(chr(idx + ord("A")))
        else:
            result.append(c)
    return "".join(result)


def vigenere_decrypt(ciphertext, key):
    result = []
    key_len = len(key)

    for i, c in enumerate(ciphertext):
        if c in ALPHABET:
            shift = ord(key[i % key_len]) - ord("A")
            idx = (ord(c) - ord("A") - shift) % 26
            result.append(chr(idx + ord("A")))
        else:
            result.append(c)

    return "".join(result)


def score_text(text):
    # higher score = more likely Portuguese
    score = 0
    for letter in PORTUGUESE_FREQ_ORDER[:6]:
        score += text.count(letter)
    return score


def best_caesar_shift(slice_text):
    best_shift = 0
    best_score = -1

    for shift in range(ALPHABET_SIZE):
        decrypted = caesar_decrypt(slice_text, shift)
        score = score_text(decrypted)

        if score > best_score:
            best_score = score
            best_shift = shift

    return best_shift


def attack_vigenere(key_length, ciphertext, words):
    # split ciphertext into slices
    slices = ["" for _ in range(key_length)]
    for i, c in enumerate(ciphertext):
        slices[i % key_length] += c

    # determine best shift per slice
    key = ""
    for slice_text in slices:
        shift = best_caesar_shift(slice_text)
        key += chr(shift + ord("A"))

    # decrypt full ciphertext
    plaintext = vigenere_decrypt(ciphertext, key)

    # check if any provided word exists
    for w in words:
        if w in plaintext:
            return key, plaintext

    return None


def main():
    if len(sys.argv) < 4:
        return

    key_length = int(sys.argv[1])
    ciphertext = sys.argv[2].upper()
    words = [w.upper() for w in sys.argv[3:]]

    result = attack_vigenere(key_length, ciphertext, words)

    if result:
        key, plaintext = result
        print(key)
        print(plaintext)


if __name__ == "__main__":
    main()
