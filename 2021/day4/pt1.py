#!/usr/bin/env python

import numpy as np


def read_input(filename):
    """
    >>> draws, grids = read_input('example')
    >>> ','.join(str(d) for d in draws)
    '7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1'
    >>> len(grids)
    3
    >>> len(grids[0])
    5
    >>> len(grids[0][0])
    5
    >>> grids[2][4]
    array([ 2,  0, 12,  3,  7])
    """
    draws = []
    grids = []

    with open(filename) as fd:
        draws = [int(draw) for draw in fd.readline().strip().split(",")]

        grid = []
        for rowstr in fd.readlines():
            if len(rowstr.strip()) == 0:
                if len(grid):
                    grids.append(grid)
                grid = []
            else:
                grid.append([int(n) for n in rowstr.strip().split()])
        if len(grid):
            grids.append(grid)

    return draws, np.array(grids)


def is_done(grid):
    """Meh
    """
    ROWS, COLS = grid.shape
    for x in range(COLS):
        if np.all(grid[:, x] == -99):
            return True
    for y in range(ROWS):
        if np.all(grid[y, :] == -99):
            return True
    return False


def main(draws, grids):
    """
    >>> draws, grids = read_input('example')
    >>> main(draws, grids)
    (24, 188, 4512)
    """
    for draw in draws:
        grids[grids == draw] = -99
        GRIDS, _, _ = grids.shape
        for g in range(GRIDS):
            grid = grids[g]
            if is_done(grid):
                _sum = np.sum(grid[grid >= 0])
                return draw, _sum, _sum * draw
    return None


if __name__ == "__main__":
    print(main(*read_input("input")))
