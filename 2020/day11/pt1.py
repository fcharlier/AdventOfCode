#!/usr/bin/env python

import numpy

EXAMPLE = """L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL
"""

ROUND1 = """#.##.##.##
#######.##
#.#.#..#..
####.##.##
#.##.##.##
#.#####.##
..#.#.....
##########
#.######.#
#.#####.##
"""

ROUND2 = """#.LL.L#.##
#LLLLLL.L#
L.L.L..L..
#LLL.LL.L#
#.LL.LL.LL
#.LLLL#.##
..L.L.....
#LLLLLLLL#
#.LLLLLL.L
#.#LLLL.##
"""

ROUND3 = """#.##.L#.##
#L###LL.L#
L.#.#..#..
#L##.##.L#
#.##.LL.LL
#.###L#.##
..#.#.....
#L######L#
#.LL###L.L
#.#L###.##
"""

ROUND4 = """#.#L.L#.##
#LLL#LL.L#
L.L.L..#..
#LLL.##.L#
#.LL.LL.LL
#.LL#L#.##
..L.L.....
#L#LLLL#L#
#.LLLLLL.L
#.#L#L#.##
"""

ROUND5 = """#.#L.L#.##
#LLL#LL.L#
L.#.L..#..
#L##.##.L#
#.#L.LL.LL
#.#L#L#.##
..L.L.....
#L#L##L#L#
#.LLLLLL.L
#.#L#L#.##
"""


def input2array(_in):
    return numpy.array([list(line) for line in _in.strip().split()])


def occupied_around(seats, row, col):
    up = max(row - 1, 0)
    down = min(row + 2, len(seats))
    left = max(col - 1, 0)
    right = min(col + 2, len(seats[0]))
    around = seats[up:down, left:right]
    seat_occupied = 1 if seats[row, col] == "#" else 0
    return numpy.sum(around == "#") - seat_occupied


def placement_round(seats):
    """Meh
    >>> r1 = placement_round(input2array(EXAMPLE))
    >>> numpy.all(r1 == input2array(ROUND1))
    True
    >>> r2 = placement_round(r1)
    >>> numpy.all(r2 == input2array(ROUND2))
    True
    >>> r3 = placement_round(r2)
    >>> numpy.all(r3 == input2array(ROUND3))
    True
    >>> r4 = placement_round(r3)
    >>> numpy.all(r4 == input2array(ROUND4))
    True
    >>> r5 = placement_round(r4)
    >>> numpy.all(r5 == input2array(ROUND5))
    True
    """
    result = numpy.array(seats, copy=True)
    for (row, col), seat in numpy.ndenumerate(seats):
        occupied = occupied_around(seats, row, col)
        if seat == "L" and occupied == 0:
            result[row, col] = "#"
            continue
        if seat == "#" and occupied >= 4:
            result[row, col] = "L"
            continue

    return result


def stabilize(seats):
    """Meh
    >>> stabilize(input2array(EXAMPLE))
    37
    """
    previous = seats
    r = placement_round(previous)

    while not numpy.all(r == previous):
        previous = r
        r = placement_round(previous)

    return numpy.sum(r == "#")


if __name__ == "__main__":
    with open("input") as fd:
        seats = input2array(fd.read())

    print(stabilize(seats))
