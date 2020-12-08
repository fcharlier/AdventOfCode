#!/usr/bin/python

from itertools import permutations


def load(fi):
    """
    >>> load('adv2017-2_test-data')
    [[5, 1, 9, 5], [7, 5, 3], [2, 4, 6, 8]]
    """
    with open(fi) as fd:
        return [map(int, line.strip().split('\t')) for line in fd]


def line_max(line):
    """
    >>> line_max([5, 1, 9, 5])
    9
    >>> line_max([7, 5, 3])
    7
    """
    return max(line)


def line_min(line):
    """
    >>> line_min([5, 1, 9, 5])
    1
    >>> line_min([7, 5, 3])
    3
    """
    return min(line)


def line_diff(line):
    """
    >>> line_diff([5, 1, 9, 5])
    8
    >>> line_diff([7, 5, 3])
    4
    >>> line_diff([2, 4, 6, 8])
    6
    """
    return max(line) - min(line)


def hash(array):
    """
    >>> hash([[5, 1, 9, 5], [7, 5, 3], [2, 4, 6, 8]])
    18
    """
    return sum(line_diff(line) for line in array)


def line_div(line):
    for seq in permutations(line, 2):
        if seq[0] % seq[1] == 0:
            return seq[0] / seq[1]


def hash2(array):
    return sum(line_div(line) for line in array)


def hash_fi(filename, func):
    return func(load(filename))


if __name__ == '__main__':
    print hash_fi('adv2017-2_puzzle-input', hash)
    print hash_fi('adv2017-2_puzzle-input', hash2)
