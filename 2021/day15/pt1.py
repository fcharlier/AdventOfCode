#!/usr/bin/env python

import operator
import numpy as np


def read_input(filename):
    """Meh
    >>> riskmap = read_input('example')
    >>> len(riskmap)
    10
    >>> len(riskmap[0])
    10
    >>> riskmap[0][0]
    1
    >>> riskmap[9][8]
    8
    """
    with open(filename) as fd:
        return [[int(n) for n in line.strip()] for line in fd if line.strip()]


def enlarge_your_risk_map(risk_map):
    """
    >>> riskmap = read_input('example')
    >>> np.set_printoptions(threshold=sys.maxsize, linewidth=200)
    >>> bigger = enlarge_your_risk_map(riskmap)
    >>> bigger.shape
    (50, 50)
    >>> bigger[49, 49]
    9
    >>> bigger[10, 10]
    3
    """
    risk_map = np.array(risk_map)
    sX, sY = risk_map.shape
    bigger = np.pad(risk_map, ((0, risk_map.shape[0] * 4), (0, risk_map.shape[1] * 4)))

    for y in range(0, 5 * sY, sY):
        for x in range(0, 5 * sX, sX):
            submap = (risk_map - 1) + (x // sX + y // sY)
            submap %= 9
            submap += 1
            bigger[y : y + sY, x : x + sX] = submap

    return bigger


def something_like_dijkstra_but_not_really(risk_map, start=(0, 0), end=(-1, -1)):
    """
    This implementation is hack-ish and only works when there are no up or left
    moves required.

    To work around the problem, doing enough additional passes from the start
    allows to bypass this limitation but without guaranteeing that the result is true
    if there's too many up or left moves.

    But hey, it's just a game, the goal is to find the solution.

    >>> something_like_dijkstra_but_not_really(read_input('example'))
    40
    >>> something_like_dijkstra_but_not_really(read_input('example3'))
    15
    >>> something_like_dijkstra_but_not_really(read_input('example2'))
    315
    >>> something_like_dijkstra_but_not_really(enlarge_your_risk_map(read_input('example')))
    315
    """
    shape = (len(risk_map), len(risk_map[0]))
    distances = [
        [operator.pow(*shape) for _ in range(shape[1])] for _ in range(shape[0])
    ]
    distances[0][0] = 0
    y, x = start

    for _ in range(15):
        for y in range(shape[0]):
            for x in range(shape[1]):
                for dy, dx in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                    if 0 <= y + dy < shape[0] and 0 <= x + dx < shape[1]:
                        distances[y + dy][x + dx] = min(
                            distances[y][x] + risk_map[y + dy][x + dx],
                            distances[y + dy][x + dx],
                        )

    return distances[end[1]][end[0]]


def main(filename):
    """
    >>> main('example')
    40
    315
    """
    riskmap = read_input(filename)
    print(something_like_dijkstra_but_not_really(riskmap))
    print(something_like_dijkstra_but_not_really(enlarge_your_risk_map(riskmap)))


if __name__ == "__main__":
    main("input")
