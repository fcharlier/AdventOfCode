#!/usr/bin/python3

from functools import reduce
from operator import mul


def read_input(filename):
    """Reads contents of filename and returns a useful data structure
    >>> heightmap = read_input("input_example")
    >>> len(heightmap)
    5
    >>> len(heightmap[0])
    5
    >>> heightmap[2][0]
    6
    >>> heightmap[3][4]
    9
    """
    with open(filename) as fd:
        return [[int(digit) for digit in line.strip()] for line in fd if len(line) > 1]


def scenic_score(heightmap, row, col):
    """Returns the scenic score of the tree at (row, col).
    >>> heightmap = read_input("input_example")
    >>> scenic_score(heightmap, 1, 2)
    4
    >>> scenic_score(heightmap, 3, 2)
    8
    """
    if (
        row == 0
        or col == 0
        or row == len(heightmap) - 1
        or col == len(heightmap[0]) - 1
    ):
        return True

    fromleft = [heightmap[row][c] < heightmap[row][col] for c in range(col)][::-1]
    fromright = [
        heightmap[row][c] < heightmap[row][col] for c in range(col + 1, len(heightmap[row]))
    ]
    fromtop = [heightmap[r][col] < heightmap[row][col] for r in range(row)][::-1]
    frombottom = [
        heightmap[r][col] < heightmap[row][col] for r in range(row + 1, len(heightmap))
    ]

    def side_score(side_view):
        score = 0
        for view in side_view:
            if view:
                score += 1
            else:
                score += 1
                break
        return score

    scores = [side_score(side) for side in (fromtop, fromright, fromleft, frombottom)]

    return reduce(mul, scores, 1)


def max_scenic_score(heightmap):
    """Returns the maximum scenic score
    >>> heightmap = read_input("input_example")
    >>> max_scenic_score(heightmap)
    8
    """
    scores = []
    for row in range(len(heightmap)):
        for col in range(len(heightmap[0])):
            scores.append(scenic_score(heightmap, row, col))
    return max(scores)


if __name__ == '__main__':
    heightmap = read_input("input_real")
    print(max_scenic_score(heightmap))
