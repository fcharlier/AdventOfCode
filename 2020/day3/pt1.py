#!/usr/bin/env python


def readinput(path):
    with open(path) as fd:
        return fd.readlines()


def countTreesForSlope(toboggan, slope):
    """Meh
    >>> countTreesForSlope(readinput("sample"), (3, 1))
    7
    >>> countTreesForSlope(readinput("sample"), (1, 1))
    2
    >>> countTreesForSlope(readinput("sample"), (5, 1))
    3
    >>> countTreesForSlope(readinput("sample"), (7, 1))
    4
    >>> countTreesForSlope(readinput("sample"), (1, 2))
    2
    """
    pos = [0, 0]
    width = len(toboggan[0]) - 1  # don't count the ending '\n'
    trees = 0
    while pos[1] < len(toboggan):
        if toboggan[pos[1]][pos[0] % width] == "#":
            trees += 1
        pos[0] += slope[0]
        pos[1] += slope[1]
    return trees


if __name__ == "__main__":
    data = readinput("input")
    trees = countTreesForSlope(data, (3, 1))
    print(f"Part 1: {trees} encountered down the slope")

    answer = 1
    for slope in ((1, 1), (3, 1), (5, 1), (7, 1), (1, 2)):
        answer *= countTreesForSlope(data, slope)
    print(f"Part 2: {answer}")
