#!/usr/bin/env python

import functools
import itertools
import operator


def meh(expenses, n):
    """Meh
    >>> meh((1721, 979, 366, 299, 675, 1456), 2)
    514579
    >>> meh((1721, 979, 366, 299, 675, 1456), 3)
    241861950
    """
    for ex in itertools.combinations(expenses, n):
        if functools.reduce(operator.add, ex) == 2020:
            return functools.reduce(operator.mul, ex)


if __name__ == "__main__":
    with open("input1") as fd:
        expenses = list(int(n) for n in fd.readlines())
    print(meh(expenses, 2))
    print(meh(expenses, 3))
