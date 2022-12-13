#!/usr/bin/python3

from ast import literal_eval
from functools import cmp_to_key
from itertools import zip_longest
from operator import mul


def in_order(left, right):
    """
    >>> in_order([1,1,3,1,1], [1,1,5,1,1])
    -1
    >>> in_order([[1],[2,3,4]], [[1],4])
    -1
    >>> in_order([9], [[8,7,6]])
    1
    >>> in_order([[4,4],4,4], [[4,4],4,4,4])
    -1
    >>> in_order([7,7,7,7], [7,7,7])
    1
    >>> in_order([], [3])
    -1
    >>> in_order([[[]]], [[]])
    1
    >>> in_order([1,[2,[3,[4,[5,6,7]]]],8,9], [1,[2,[3,[4,[5,6,0]]]],8,9])
    1
    >>> in_order([[],7], [[3]])
    -1
    """
    for lft, rgt in zip_longest(left, right):
        if isinstance(lft, int) and isinstance(rgt, int):
            if lft > rgt:
                return 1
            if lft < rgt:
                return -1
        elif isinstance(lft, list) and isinstance(rgt, list):
            if (result := in_order(lft, rgt)) != 0:
                return result
        elif isinstance(lft, list) and isinstance(rgt, int):
            if (
                result := in_order(
                    lft,
                    [
                        rgt,
                    ],
                )
            ) != 0:
                return result
        elif isinstance(lft, int) and isinstance(rgt, list):
            if (
                result := in_order(
                    [
                        lft,
                    ],
                    rgt,
                )
            ) != 0:
                return result
        elif lft is None and rgt is not None:
            return -1
        elif lft is not None and rgt is None:
            return 1
    return 0


def read_input(filename):
    """
    >>> packets = read_input("input_example")
    >>> len(packets)
    18
    >>> packets[0]
    [1, 1, 3, 1, 1]
    >>> packets[12]
    [[[]]]
    """
    elts = []
    with open(filename) as fd:
        for line in fd:
            line = line.strip()
            if not len(line):
                continue
            elts.append(literal_eval(line))
    elts.append([[2]])
    elts.append([[6]])

    return elts


def decoder_key(packets):
    """
    >>> packets = read_input("input_example")
    >>> decoder_key(packets)
    (10, 14)
    """
    srtd = sorted(packets, key=cmp_to_key(in_order))
    return srtd.index([[2]]) + 1, srtd.index([[6]]) + 1


if __name__ == "__main__":
    packets = read_input("input_real")
    print(mul(*decoder_key(packets)))
