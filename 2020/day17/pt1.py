#!/usr/bin/env python

import numpy as np
from scipy import ndimage
import sys

# ar = np.ones((1, 3, 3), dtype=int)
# ar = np.pad(ar, 1)

# w = np.ones((3, 3, 3), dtype=int)
# w[1][1][1] = 0
# ndimage.convolve(ar, w, mode="constant", cval=0)

TEST = """.#.
..#
###
"""

np.set_printoptions(threshold=sys.maxsize)


def make_pocket(text):
    """
    >>> make_pocket(TEST)
    array([[[0, 1, 0],
            [0, 0, 1],
            [1, 1, 1]]])
    """
    data = [[1 if c == "#" else 0 for c in line] for line in text.strip().split()]
    return np.array([data], dtype=int)


def cycle(pocket, cycles):
    """Meh
    >>> cycle(make_pocket(TEST), 6)
    112
    """
    w = np.ones((3, 3, 3), dtype=int)
    w[1, 1, 1] = 0
    # print(pocket)
    for n in range(cycles):
        # print("="*12, f"Cycle {n}")
        pocket = np.pad(pocket, 1)
        neig_count = ndimage.convolve(pocket, w, mode="constant", cval=0)
        for idx, neighbors in np.ndenumerate(neig_count):
            if pocket[idx] == 1 and neighbors not in (2, 3):
                pocket[idx] = 0
            elif pocket[idx] == 0 and neighbors == 3:
                pocket[idx] = 1
        # print(pocket)

    return np.count_nonzero(pocket)


if __name__ == "__main__":
    with open("input") as fd:
        print(cycle(make_pocket(fd.read()), 6))
