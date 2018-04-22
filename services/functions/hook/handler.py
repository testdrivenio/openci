import sys


def get_stdin():
    buf = ''
    for line in sys.stdin:
        buf = buf + line
    return buf


def main():
    print(get_stdin())


if __name__ == '__main__':
    main()
