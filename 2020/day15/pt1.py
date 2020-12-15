#!/usr/bin/env python

import numpy as np


def speak_numbers(initial, count):
    """This is a naive version, should work for small-ish # of iterations.
    Might be a memory hog and slow for larger # of iterations.
    >>> speak_numbers(np.array([0, 3, 6]), 10)
    0
    >>> speak_numbers(np.array([1, 3, 2]), 2020)
    1
    >>> speak_numbers(np.array([2, 1, 3]), 2020)
    10
    >>> speak_numbers(np.array([1, 2, 3]), 2020)
    27
    >>> speak_numbers(np.array([2, 3, 1]), 2020)
    78
    >>> speak_numbers(np.array([3, 2, 1]), 2020)
    438
    >>> speak_numbers(np.array([3, 1, 2]), 2020)
    1836
    """
    for n in range(len(initial), count):
        search = initial[-1]
        latest = np.where(initial[:-1] == search)[0]
        if len(latest):
            nextnum = n - (latest[-1] + 1)  # Adding 1 because of 0 based index
        else:
            nextnum = 0
        initial = np.append(initial, nextnum)

    return initial[-1]


if __name__ == "__main__":
    with open("input") as fd:
        initial = np.array([int(n.strip()) for n in fd.read().strip().split(",")])
    print(speak_numbers(initial, 2020))
