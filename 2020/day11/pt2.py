#!/usr/bin/env python

import numpy

CANSEE1 = """.......#.
...#.....
.#.......
.........
..#L....#
....#....
.........
#........
...#.....
"""

CANSEE2 = """.............
.L.L.#.#.#.#.
.............
"""

CANSEE3 = """.##.##.
#.#.#.#
##...##
...L...
##...##
#.#.#.#
.##.##.
"""

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

ROUND2 = """#.LL.LL.L#
#LLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLL#
#.LLLLLL.L
#.LLLLL.L#
"""

ROUND3 = """#.L#.##.L#
#L#####.LL
L.#.#..#..
##L#.##.##
#.##.#L.##
#.#####.#L
..#.#.....
LLL####LL#
#.L#####.L
#.L####.L#
"""

ROUND4 = """#.L#.L#.L#
#LLLLLL.LL
L.L.L..#..
##LL.LL.L#
L.LL.LL.L#
#.LLLLL.LL
..L.L.....
LLLLLLLLL#
#.LLLLL#.L
#.L#LL#.L#
"""

ROUND5 = """#.L#.L#.L#
#LLLLLL.LL
L.L.L..#..
##L#.#L.L#
L.L#.#L.L#
#.L####.LL
..#.#.....
LLL###LLL#
#.LLLLL#.L
#.L#LL#.L#
"""

ROUND6 = """#.L#.L#.L#
#LLLLLL.LL
L.L.L..#..
##L#.#L.L#
L.L#.LL.L#
#.LLLL#.LL
..#.L.....
LLL###LLL#
#.LLLLL#.L
#.L#LL#.L#
"""


def input2array(_in):
    return numpy.array([list(line) for line in _in.strip().split()])


def can_see_direction(seats, row, col, rowdir, coldir):
    row += rowdir
    col += coldir
    (rowmax, colmax) = seats.shape
    while 0 <= row < rowmax and 0 <= col < colmax:
        if seats[row, col] == "#":
            return 1
        if seats[row, col] == "L":
            return 0

        row += rowdir
        col += coldir
    # Out of the loop we didn't find any seat
    return 0


def can_see(seats, row, col):
    """Meh
    >>> can_see(input2array(CANSEE1), 4, 3)
    8
    >>> can_see(input2array(CANSEE2), 1, 1)
    0
    >>> can_see(input2array(CANSEE3), 3, 3)
    0
    """
    directions = (
        (0, 1),
        (0, -1),
        (1, 0),
        (-1, 0),
        (1, 1),
        (1, -1),
        (-1, 1),
        (-1, -1),
    )
    return sum(
        (
            can_see_direction(seats, row, col, rowdir, coldir)
            for rowdir, coldir in directions
        )
    )


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
    >>> r6 = placement_round(r5)
    >>> numpy.all(r6 == input2array(ROUND6))
    True
    """
    result = numpy.array(seats, copy=True)
    for (row, col), seat in numpy.ndenumerate(seats):
        see_occupied = can_see(seats, row, col)
        if seat == "L" and see_occupied == 0:
            result[row, col] = "#"
            continue
        if seat == "#" and see_occupied >= 5:
            result[row, col] = "L"
            continue

    return result


def stabilize(seats):
    """Meh
    >>> stabilize(input2array(EXAMPLE))
    26
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
