#!/usr/bin/env python


import sys


def read_input(filename):
    """
    >>> read_input('example')[0]
    [(0, 0), (0, 3), (1, 0), (2, 0), (2, 1), (2, 4), (3, 2), (4, 2), (4, 3), (4, 4)]
    >>> len(read_input('example_step1')[0])
    24
    >>> len(read_input('example_step2')[0])
    35
    """
    with open(filename) as fds:
        algo = fds.readline().strip()
        _ = fds.readline()
        lights = []
        for linenum, line in enumerate(fds.readlines()):
            for colnum, char in enumerate(line.strip()):
                if char == "#":
                    lights.append((linenum, colnum))
        return lights, algo


def enhance(lights, algo):
    """
    >>> lights, algo = read_input('example')
    >>> len(lights)
    10
    >>> lights = enhance(lights, algo)
    >>> len(lights)
    24
    >>> lights = enhance(lights, algo)
    >>> len(lights)
    35
    >>> lights, algo = read_input('example_step1')
    >>> lights = enhance(lights, algo)
    >>> len(lights)
    35
    """
    minX, maxX, minY, maxY = (sys.maxsize, 0, sys.maxsize, 0)
    for light in lights:
        minX = min(minX, light[1])
        maxX = max(maxX, light[1])
        minY = min(minX, light[0])
        maxY = max(maxX, light[0])

    out = []
    for Y in range(minY - 4, maxY + 5):
        for X in range(minX - 4, maxX + 5):
            binval = 0
            for dy in range(-1, 2):
                for dx in range(-1, 2):
                    binval <<= 1
                    if (Y + dy, X + dx) in lights:
                        binval |= 0b1
            # print(algo[binval], end="")
            if algo[binval] == "#":
                out.append((Y, X))
        # print("")
    return out


if __name__ == "__main__":
    lights, algo = read_input("input")
    for n in range(2):
        lights = enhance(lights, algo)
    # Ahahahaha stupid *infinite* algo …
    minX, maxX, minY, maxY = 0, 0, 0, 0
    for light in lights:
        minX = min(minX, light[1])
        maxX = max(maxX, light[1])
        minY = min(minX, light[0])
        maxY = max(maxX, light[0])

    #
    # *khof* handle special case when pixels get lit when pixels around are dark, aka
    # the borders of the infinite
    #
    sublights = [
        light
        for light in lights
        if minX + 3 < light[1] < maxX - 4 and minY + 3 < light[0] < maxY - 4
    ]


    # for Y in range(minY + 3, maxY - 4):
    #     for X in range(minX + 3, maxX - 4):
    #         if (X, Y) in sublights:
    #             print("#", end="")
    #         else:
    #             print(".", end="")
    #     print("")

    print(len(sublights))
