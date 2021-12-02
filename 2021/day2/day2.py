#!/usr/bin/env python

EX_INPUT = """forward 5
down 5
forward 8
up 3
down 8
forward 2
"""


def move1(course):
    """Meh
    >>> move1(EX_INPUT.split('\\n'))
    (15, 10, 150)
    """
    horiz = 0
    depth = 0

    for mvt in course:
        if not len(mvt):
            continue
        where, count = mvt.split(" ")
        count = int(count)
        if where == "forward":
            horiz += count
        elif where == "down":
            depth += count
        elif where == "up":
            depth -= count

    return (horiz, depth, horiz * depth)


def move2(course):
    """Meh
    >>> move2(EX_INPUT.split('\\n'))
    (15, 60, 900)
    """
    horiz = 0
    depth = 0
    aim = 0

    for mvt in course:
        if not len(mvt):
            continue
        where, count = mvt.split(" ")
        count = int(count)
        if where == "forward":
            horiz += count
            depth += aim * count
        elif where == "down":
            aim += count
        elif where == "up":
            aim -= count

    return (horiz, depth, horiz * depth)


if __name__ == "__main__":
    with open("input") as fd:
        course = fd.read().split("\n")
    print(move1(course))
    print(move2(course))
