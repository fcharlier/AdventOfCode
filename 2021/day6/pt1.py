#!/usr/bin/env python

""" Meh
"""

import numpy as np


def read_input(filename):
    """
    >>> read_input('example')
    array([3, 4, 3, 1, 2])
    """
    with open(filename) as fd:
        return np.array([int(n) for n in fd.read().split(",")])


def next_day(fishes):
    """Meh
    >>> fishes = read_input('example')
    >>> fishes = next_day(fishes)
    >>> fishes
    array([2, 3, 2, 0, 1])
    >>> fishes = next_day(fishes)
    >>> fishes
    array([1, 2, 1, 6, 0, 8])
    >>> fishes = read_input('example')
    >>> for n in range(18):
    ...   fishes = next_day(fishes)
    >>> fishes.shape
    (26,)
    >>> for n in range(62):
    ...   fishes = next_day(fishes)
    >>> fishes.shape
    (5934,)
    >>> for n in range(176):
    ...   fishes = next_day(fishes)
    """
    fishes -= 1
    breeding = len(fishes[fishes < 0])
    if breeding:
        fishes[fishes < 0] = 6
        fishes = np.concatenate((fishes, [8] * breeding))
    return fishes


if __name__ == "__main__":
    fishes = read_input("input")
    for n in range(80):
        fishes = next_day(fishes)
    print(fishes.shape)
