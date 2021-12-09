#!/usr/bin/env python

import numpy as np


def read_input(filename):
    """
    >>> heightmap = read_input('example')
    >>> heightmap.shape
    (7, 12)
    >>> heightmap[4,4]
    7
    """
    with open(filename) as fd:
        return np.pad(
            np.array([[int(n) for n in line.strip()] for line in fd.readlines()]),
            1,
            "maximum",
        )


def lowspots(hmap):
    """Meh
    >>> list(lowspots(read_input('example')))
    [(1, 2), (1, 10), (3, 3), (5, 7)]
    """
    for y in range(1, hmap.shape[0] - 1):
        for x in range(1, hmap.shape[1] - 1):
            lowtest = (
                hmap[y, x] < hmap[y + dy, x + dx]
                for dx, dy in ((0, 1), (1, 0), (0, -1), (-1, 0))
            )
            if all(lowtest):
                yield (y, x)


def sum_lowspots(hmap):
    """
    >>> sum_lowspots(read_input('example'))
    15
    """
    return sum([hmap[y, x] + 1 for y, x in lowspots(hmap)])


def basin_around(hmap, spot):
    """
    >>> hmap = read_input('example')
    >>> basin_around(hmap, (1, 2))
    3
    >>> basin_around(hmap, (1, 10))
    9
    >>> basin_around(hmap, (3, 3))
    14
    >>> basin_around(hmap, (5, 7))
    9
    """
    n = 0
    tovisit = [spot]
    while len(tovisit) > 0:
        y, x = tovisit.pop(0)
        if hmap[y, x] < 9:
            n += 1
            hmap[y, x] = 9
            # Save above & below for later
            for v in (-1, 1):
                if hmap[y + v, x] < 9:
                    tovisit.append((y + v, x))

            l = x - 1
            r = x + 1

            while hmap[y, l] < 9:
                n += 1
                hmap[y, l] = 9
                for v in (-1, 1):
                    if hmap[y + v, l] < 9:
                        tovisit.append((y + v, l))
                l -= 1

            while hmap[y, r] < 9:
                n += 1
                hmap[y, r] = 9
                for v in (-1, 1):
                    if hmap[y + v, r] < 9:
                        tovisit.append((y + v, r))
                r += 1
    return n


def greatest_basins(hmap, count=3):
    """
    >>> hmap = read_input('example')
    >>> greatest_basins(hmap, 3)
    1134
    """
    basins = []
    for lowspot in lowspots(hmap):
        basins.append(basin_around(hmap, lowspot))
    return np.prod(sorted(basins, reverse=True)[:3])


if __name__ == "__main__":
    hmap = read_input("input")
    print(sum_lowspots(hmap))
    print(greatest_basins(hmap))
