#!/usr/bin/env python

""" Meh
"""

import numpy as np


def load_input(filename):
    """
    >>> lines = load_input('example')
    >>> len(lines)
    10
    >>> lines[0]
    [[0, 9], [5, 9]]
    >>> lines[8]
    [[0, 0], [8, 8]]
    """
    lines = []
    with open(filename) as fd:
        for line in fd:
            if len(line.strip()):
                start, end = line.strip().split(" -> ")
                lines.append(
                    [
                        [int(n) for n in start.split(",")],
                        [int(n) for n in end.split(",")],
                    ]
                )
    return lines


def filter_hv(lines):
    """Meh
    >>> hv = filter_hv(load_input('example'))
    >>> len(list(hv))
    6
    """
    for (sx, sy), (ex, ey) in lines:
        if sx == ex or sy == ey:
            yield ([[sx, sy], [ex, ey]])


def shape(lines):
    """
    >>> shape(filter_hv(load_input('example')))
    (0, 0, 10, 10)
    """
    minx, miny, maxx, maxy = 999, 999, 0, 0

    for (sx, sy), (ex, ey) in lines:
        minx = min(sx, ex, minx)
        maxx = max(sx, ex, maxx)
        miny = min(sy, ey, miny)
        maxy = max(sy, ey, maxy)

    return minx, miny, maxx + 1, maxy + 1


def make_np_arr(lines):
    """Meh
    >>> arr = make_np_arr(load_input('example'))
    >>> arr.shape
    (10, 10)
    >>> np.all(arr == 0)
    True
    """
    shp = shape(lines)
    return np.zeros((shp[3], shp[2]), dtype=int)


def draw_lines(fmap, lines):
    """Meh
    >>> lines = load_input('example')
    >>> lineshv = list(filter_hv(lines))
    >>> fumeshv = make_np_arr(lineshv)
    >>> draw_lines(fumeshv, lineshv)
    >>> len(fumeshv[fumeshv > 1])
    5
    >>> np.all(fumeshv[fumeshv > 1] == 2)
    True
    >>> fumesx = make_np_arr(lines)
    >>> draw_lines(fumesx, lines)
    >>> len(fumesx[fumesx > 1])
    12
    """
    for (sx, sy), (ex, ey) in lines:
        if sx == ex:
            sy, ey = min(sy, ey), max(sy, ey)
            fmap[sy:ey + 1, sx] += 1
        elif sy == ey:
            sx, ex = min(sx, ex), max(sx, ex)
            fmap[sy, sx:ex + 1] += 1
        else:
            yinc = 1 if ey > sy else -1
            xinc = 1 if ex > sx else -1
            for n in range((ex - sx) * xinc + 1):
                fmap[sy + n * yinc, sx + n * xinc] += 1


if __name__ == "__main__":
    lines = load_input("input")
    fumesmap = make_np_arr(lines)
    draw_lines(fumesmap, filter_hv(lines))
    print("Pt1:", len(fumesmap[fumesmap > 1]))
    fumesmap = make_np_arr(lines)
    draw_lines(fumesmap, lines)
    print("Pt2:", len(fumesmap[fumesmap > 1]))


