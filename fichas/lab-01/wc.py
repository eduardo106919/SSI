import sys


def wc(filename):
    with open(filename, "r") as file:
        content = file.read()
        chars = len(content)
        lines = content.splitlines()
        temp = [l.split() for l in lines]
        words = 0
        for lw in temp:
            words += len(lw)

        return (len(lines), words, chars)


def main(inp):
    inp.pop(0)
    total = [0, 0, 0]
    for f in inp:
        l, w, c = wc(f)
        print(f"{l:4} {w:4} {c:4} {f}")
        total[0] += l
        total[1] += w
        total[2] += c

    if len(inp) > 1:
        print(f"{total[0]:4} {total[1]:4} {total[2]:4} total")


if __name__ == "__main__":
    main(sys.argv)
