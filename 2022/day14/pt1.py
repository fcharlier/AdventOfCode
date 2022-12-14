#!/usr/bin/python3

from itertools import pairwise
import sys

import numpy as np


def read_input(filename):
    """
    >>> lines = read_input("input_example")
    >>> len(lines)
    5
    >>> lines[0]
    ((498, 4), (498, 6))
    >>> lines[1]
    ((498, 6), (496, 6))
    >>> lines[2]
    ((503, 4), (502, 4))
    """
    lines = []
    with open(filename) as fd:
        for text in fd:
            lines.extend(
                tuple(tuple(map(int, point.split(","))) for point in line)
                for line in pairwise(text.strip().split(" -> "))
            )

    return lines


def max_rock_depth(lines):
    """
    >>> lines = read_input("input_example")
    >>> max_rock_depth(lines)
    9
    """
    return max(point[1] for line in lines for point in line)


def minmax_sides(lines):
    """
    >>> lines = read_input("input_example")
    >>> minmax_sides(lines)
    (494, 503)
    """
    side_min = sys.maxsize
    side_max = 0
    for line in lines:
        for point in line:
            side_max = max(side_max, point[0])
            side_min = min(side_min, point[0])
    return (side_min, side_max)


def get_cave_map(lines):
    """
    >>> lines = read_input("input_example")
    >>> cave_map, shiftX = get_cave_map(lines)
    """
    depth = max_rock_depth(lines)
    left, right = minmax_sides(lines)

    cave_map = np.chararray((right - left + 1, depth + 1))
    cave_map.fill(".")
    for line in lines:
        if line[0][0] > line[1][0] or line[0][1] > line[1][1]:
            line = (line[1], line[0])
        cave_map[
            line[0][0] - left : line[1][0] - left + 1, line[0][1] : line[1][1] + 1
        ] = "#"

    return cave_map, left


def drop_sand(cave_map, shiftX, start_pos=(500, 0)):
    """
    >>> lines = read_input("input_example")
    >>> cave_map, shiftX = get_cave_map(lines)
    >>> drop_sand(cave_map, shiftX)
    24
    """
    X, Y = start_pos
    X -= shiftX
    max_depth = cave_map.shape[1] - 1
    count = 0

    while 0 <= X < cave_map.shape[0] and Y < max_depth and cave_map[X, Y] == b".":
        nY = Y + 1
        for dX in [0, -1, 1]:
            nX = X + dX
            if nX < 0 or nX >= cave_map.shape[0] or nY > max_depth:
                return count
            if cave_map[nX, nY] == b".":
                X, Y = nX, nY
                break

        if Y < nY:
            cave_map[X, Y] = b"o"
            count += 1
            X, Y = start_pos
            X -= shiftX
    return count


if __name__ == "__main__":
    lines = read_input("input_real")
    cave_map, shiftX = get_cave_map(lines)
    print(drop_sand(cave_map, shiftX))
