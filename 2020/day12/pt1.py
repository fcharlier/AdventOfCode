#!/usr/bin/env python

"""
LOL, given how it was easier with numpy in pt2,
I should've gone for numpy from start XD
"""

from operator import add

EXAMPLE = """F10
N3
F7
R90
F11
"""


def parse_directions(text):
    return [(di[0], int(di[1:])) for di in text.strip().split()]


def rotate_right_90(vec):
    if vec == (0, 1):
        return (1, 0)
    if vec == (1, 0):
        return (0, -1)
    if vec == (0, -1):
        return (-1, 0)
    if vec == (-1, 0):
        return (0, 1)


def rotate_left_90(vec):
    if vec == (0, 1):
        return (-1, 0)
    if vec == (-1, 0):
        return (0, -1)
    if vec == (0, -1):
        return (1, 0)
    if vec == (1, 0):
        return (0, 1)


def rotate(vec, dir, count):
    if dir == "R":
        func = rotate_right_90
    if dir == "L":
        func = rotate_left_90

    for n in range(count):
        vec = func(vec)
    return vec


def move(directions):
    """Meh
    >>> move(parse_directions(EXAMPLE))
    (10, 0) (1, 0)
    (10, 3) (1, 0)
    (17, 3) (1, 0)
    (17, 3) (0, -1)
    (17, -8) (0, -1)
    25
    """
    pos = [0, 0]
    facing = (1, 0)
    for where, count in directions:
        if where == "N":
            pos[1] += count
        if where == "S":
            pos[1] -= count
        if where == "E":
            pos[0] += count
        if where == "W":
            pos[0] -= count
        if where == "F":
            pos[0] += count * facing[0]
            pos[1] += count * facing[1]
        if where in ("R", "L"):
            facing = rotate(facing, where, count // 90)
        print(pos, facing)
    return add(*[abs(p) for p in pos])


if __name__ == "__main__":
    with open("input") as fd:
        print(move(parse_directions(fd.read())))
