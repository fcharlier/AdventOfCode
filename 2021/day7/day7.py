#!/usr/bin/env python


def read_input(filename):
    """
    >>> read_input('example')
    [16, 1, 2, 0, 4, 2, 7, 1, 2, 14]
    """
    with open(filename) as fd:
        return [int(n) for n in fd.readline().strip().split(",")]


def fuelforpos(pos, crabs):
    """Meh
    >>> crabs = read_input('example')
    >>> fuelforpos(1, crabs)
    41
    >>> fuelforpos(3, crabs)
    39
    >>> fuelforpos(10, crabs)
    71
    >>> fuelforpos(2, crabs)
    37
    """
    return sum(abs(crab - pos) for crab in crabs)


def fuelformove2(src, dest):
    """Meh
    >>> fuelformove2(16, 5)
    66
    >>> fuelformove2(1, 5)
    10
    >>> fuelformove2(2, 5)
    6
    >>> fuelformove2(5, 5)
    0
    >>> fuelformove2(0, 5)
    15
    >>> fuelformove2(4, 5)
    1
    >>> fuelformove2(7, 5)
    3
    >>> fuelformove2(14, 5)
    45
    """
    count = abs(src - dest)
    return count * (count + 1) // 2


def fuelforpos2(pos, crabs):
    """Meh
    >>> crabs = read_input('example')
    >>> fuelforpos2(2, crabs)
    206
    >>> fuelforpos2(5, crabs)
    168
    """
    return sum(fuelformove2(crab, pos) for crab in crabs)


if __name__ == "__main__":
    crabs = read_input("input")
    mx = max(crabs)

    minfuel = len(crabs) * mx
    minfuel2 = len(crabs) * mx * mx
    for n in range(mx):
        ffpos = fuelforpos(n, crabs)
        ffpos2 = fuelforpos2(n, crabs)
        minfuel = min(minfuel, ffpos)
        minfuel2 = min(minfuel2, ffpos2)

    print(minfuel)
    print(minfuel2)
