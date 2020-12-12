#!/usr/bin/env python

from operator import add
import numpy as np

EXAMPLE = """F10
N3
F7
R90
F11
"""

NORTH = np.array((0, 1), dtype=int)
SOUTH = -NORTH
EAST = np.array((1, 0), dtype=int)
WEST = -EAST


def parse_directions(text):
    return [(di[0], int(di[1:])) for di in text.strip().split()]


def rotate(vec, dir, angle):
    if dir == "R":
        t = np.radians(-angle)
    if dir == "L":
        t = np.radians(angle)

    mx = np.array(((np.cos(t), -np.sin(t)), (np.sin(t), np.cos(t))), dtype=int)
    return mx.dot(vec)


def move(directions):
    """Meh
    >>> move(parse_directions(EXAMPLE))
    [100  10] [10  1]
    [100  10] [10  4]
    [170  38] [10  4]
    [170  38] [  4 -10]
    [214 -72] [  4 -10]
    286
    """
    wpt = np.array((10, 1), dtype=int)
    pos = np.array((0, 0), dtype=int)
    for where, count in directions:
        if where == "N":
            wpt += count * NORTH
        if where == "S":
            wpt += count * SOUTH
        if where == "E":
            wpt += count * EAST
        if where == "W":
            wpt += count * WEST
        if where == "F":
            pos += count * wpt
        if where in ("R", "L"):
            wpt = rotate(wpt, where, count)
        print(pos, wpt)
    return add(*[abs(p) for p in pos])


if __name__ == "__main__":
    with open("input") as fd:
        print(move(parse_directions(fd.read())))
