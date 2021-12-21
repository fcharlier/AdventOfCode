#!/usr/bin/env python


import sys
import numpy as np
from datetime import datetime


def read_input(filename):
    """
    >>> lights, algo = read_input('example')
    >>> lights.shape
    (5, 5)
    >>> len(lights[lights == True])
    10
    """
    with open(filename) as fds:
        algo = [char == "#" for char in fds.readline().strip()]
        _ = fds.readline()
        lights = np.array([[char == "#" for char in line.strip()] for line in fds])
        return lights, algo


def binval(lights):
    """
    >>> binval(np.array([[1, 0, 0], [0, 0, 0], [0, 0, 0]]))
    256
    >>> binval(np.array([[0, 1, 0], [0, 0, 0], [0, 0, 0]]))
    128
    >>> binval(np.array([[0, 1, 0], [0, 0, 0], [0, 0, 1]]))
    129
    """
    value = 0
    for light in np.nditer(lights):
        value <<= 1
        value |= 1 | 1 if light else 0
    return value


def enhance(lights, algo, count):
    """
    >>> lights, algo = read_input('example')
    >>> enhance(lights, algo, 1)
    24
    >>> enhance(lights, algo, 2)
    35
    >>> lights, algo = read_input('example')
    >>> enhance(lights, algo, 50)
    3351
    """

    lights = np.pad(lights, count + 6, constant_values=False)
    sizeY, sizeX = lights.shape
    # for Y in range(sizeY):
    #     for X in range(sizeX):
    #         print("#" if lights[Y, X] else ".", end="")
    #     print("")

    for n in range(count, 0, -1):
        enhanced = np.ndarray(lights.shape, dtype=bool)
        enhanced.fill(False)
        for Y in range(1, sizeY):
            for X in range(1, sizeX):
                enhanced[Y, X] = algo[binval(lights[Y - 1 : Y + 2, X - 1 : X + 2])]
            #     print("#" if enhanced[Y, X] else ".", end="")
            # print("")
        lights = enhanced

    return len(lights[lights == True])


if __name__ == "__main__":
    lights, algo = read_input("input")
    print(enhance(lights, algo, 2))
    print(enhance(lights, algo, 50))
