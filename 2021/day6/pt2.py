#!/usr/bin/env python

""" Meh
Part 1 was building the list of fishes.

As the breeding is exponential, won't work for too many generations.

Instead of building the list, this time we'll count the # of fishes for each timer
"""


def read_input(filename):
    """
    >>> data = read_input('example')
    >>> data
    [0, 1, 1, 2, 1, 0, 0, 0, 0]
    >>> len(data)
    9
    """
    with open(filename) as fd:
        arr = [0] * 9
        for val in (int(n) for n in fd.read().split(",")):
            arr[val] += 1
        return arr


def next_day(fishes):
    """Meh
    >>> fishes = read_input('example')
    >>> fishes = next_day(fishes)
    >>> fishes
    [1, 1, 2, 1, 0, 0, 0, 0, 0]
    >>> fishes = next_day(fishes)
    >>> fishes
    [1, 2, 1, 0, 0, 0, 1, 0, 1]
    >>> fishes = read_input('example')
    >>> for n in range(18):
    ...   fishes = next_day(fishes)
    >>> sum(fishes)
    26
    >>> for n in range(62):
    ...   fishes = next_day(fishes)
    >>> sum(fishes)
    5934
    >>> for n in range(176):
    ...   fishes = next_day(fishes)
    >>> sum(fishes)
    26984457539
    """
    newgen = fishes[0]
    nextgen = fishes[1:] + [newgen, ]
    nextgen[6] += newgen
    return nextgen


if __name__ == "__main__":
    fishes = read_input("input")
    for n in range(256):
        fishes = next_day(fishes)
    print(sum(fishes))
