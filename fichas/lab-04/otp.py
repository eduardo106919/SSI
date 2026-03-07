import sys
import os


def setup(n_bytes, filename):
    key = os.urandom(n_bytes)
    with open(filename, "wb") as f:
        f.write(key)


def xor_files(input_file, key_file, output_suffix):
    with open(input_file, "rb") as f_in, open(key_file, "rb") as f_key:
        data = f_in.read()
        key = f_key.read()

        if len(key) < len(data):
            print("Erro: A chave é menor que a mensagem.")
            sys.exit(1)

        # Operação XOR binária entre a mensagem e a chave
        result = bytes([b_data ^ b_key for b_data, b_key in zip(data, key)])

        output_filename = input_file + output_suffix
        with open(output_filename, "wb") as f_out:
            f_out.write(result)


def main():
    if len(sys.argv) < 4:
        print("Usage:")
        print("  python3 otp.py setup <n_bytes> <key_file>")
        print("  python3 otp.py enc <msg_file> <key_file>")
        print("  python3 otp.py dec <crypt_file> <key_file>")
    else:
        mode = sys.argv[1]

        if mode == "setup":
            n_bytes = int(sys.argv[2])
            filename = sys.argv[3]
            setup(n_bytes, filename)
        elif mode == "enc":
            msg_file = sys.argv[2]
            key_file = sys.argv[3]
            xor_files(msg_file, key_file, ".enc")
        elif mode == "dec":
            crypt_file = sys.argv[2]
            key_file = sys.argv[3]
            xor_files(crypt_file, key_file, ".dec")


if __name__ == "__main__":
    main()
