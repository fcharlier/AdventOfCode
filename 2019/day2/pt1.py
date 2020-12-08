#!/usr/bin/python3


def process(intcode):
    """Processes an intcode

    >>> process([1,9,10,3,99,3,11,0,99,30,40,50])
    [1, 9, 10, 70, 99, 3, 11, 0, 99, 30, 40, 50]
    >>> process([1, 0, 0, 0, 99])
    [2, 0, 0, 0, 99]
    >>> process([2, 3, 0, 3, 99])
    [2, 3, 0, 6, 99]
    >>> process([2, 4, 4, 5, 99, 0])
    [2, 4, 4, 5, 99, 9801]
    >>> process([1, 1, 1, 4, 99, 5, 6, 0, 99])
    [30, 1, 1, 4, 2, 5, 6, 0, 99]
    """
    pos = 0
    while intcode[pos] != 99:
        op = intcode[pos]
        left = intcode[pos + 1]
        right = intcode[pos + 2]
        dest = intcode[pos + 3]
        if op == 1:
            intcode[dest] = intcode[left] + intcode[right]
        if op == 2:
            intcode[dest] = intcode[left] * intcode[right]
        pos += 4


if __name__ == "__main__":
    with open("data") as data:
        data = data.read().split(",")
        intcode = list(map(int, data))

    intcode[1] = 12
    intcode[2] = 2
    process(intcode)
    print(intcode[0])
