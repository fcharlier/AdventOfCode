#!/usr/bin/python3

import numpy as np
import numpy.ma as ma
import pandas as pd


def read_input(filename):
    """Meh"""
    with open(filename) as fd:
        return np.array([list(map(ord, list(line.strip()))) for line in fd])


def indexof(ndar, value):
    loc = np.where(ndar == value)
    return loc[0][0], loc[1][0]


def shortest_path(heights):
    """
    >>> heights = read_input("input_example")
    >>> shortest_path(heights)
    31
    """
    start = indexof(heights, ord("S"))
    end = indexof(heights, (ord("E")))

    heights[start] = ord("a")
    heights[end] = ord("z")

    closed = []
    opn = [start]
    cost = np.ndarray(heights.shape, dtype=np.int16)
    cost.fill(ma.minimum_fill_value(cost))
    cost[start] = 0

    min_len = 32768
    while len(opn):
        cur = opn.pop()

        if cur == end:
            min_len = min(cost[end], min_len)
        for dif in ((-1, 0), (1, 0), (0, 1), (0, -1)):
            neig = (cur[0] + dif[0], cur[1] + dif[1])

            if (
                0 <= neig[0] < heights.shape[0]
                and 0 <= neig[1] < heights.shape[1]
                and heights[neig] - heights[cur] <= 1
                and cost[neig] > cost[cur] + 1
            ):
                cost[neig] = cost[cur] + 1
                opn.append(neig)

        closed.append(str(cur))
    return min(min_len, ma.minimum_fill_value(cost))


if __name__ == "__main__":
    heights = read_input("input_real")
    print(shortest_path(heights))
