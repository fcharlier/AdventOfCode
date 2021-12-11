#!/usr/bin/python

import numpy as np


def read_input(filename):
    """
    >>> ar = read_input('example')
    >>> ar.shape
    (10, 10)
    >>> ar[0, 0]
    5
    >>> ar[0, 9]
    3
    >>> ar[9, 0]
    5
    >>> ar[9, 9]
    6
    """
    with open(filename) as fd:
        return np.array([[int(n) for n in line.strip()] for line in fd])


def inc_around(octos, y, x):
    for dy in range(-1, 2):
        for dx in range(-1, 2):
            if (
                0 <= y + dy < octos.shape[0]
                and 0 <= x + dx < octos.shape[1]
                and not (dx == 0 and dy == 0)
            ):
                octos[y + dy, x + dx] += 1


def make_step(octos):
    """
    >>> octos = read_input('step0')
    >>> s1 = read_input('step1')
    >>> s2 = read_input('step2')
    >>> make_step(octos)
    9
    >>> np.all(octos == s1)
    True
    >>> make_step(octos)
    0
    >>> np.all(octos == s2)
    True
    >>> octos = read_input('example')
    >>> for n in range(10):
    ...   make_step(octos)
    0
    35
    45
    16
    8
    1
    7
    24
    39
    29
    """
    octos += 1
    all_flashed = octos > 9
    new_flashed = all_flashed
    while np.any(new_flashed == True):
        for y, x in np.argwhere(new_flashed == True):
            inc_around(octos, y, x)
        new_flashed = (octos > 9) ^ all_flashed
        all_flashed |= new_flashed
    octos[octos > 9] = 0
    return len(np.argwhere(all_flashed == True))


def count_flashes(octos, steps):
    """
    >>> octos = read_input('example')
    >>> count_flashes(octos, 10)
    204
    >>> count_flashes(read_input('example'), 100)
    1656
    """
    total = 0
    for n in range(steps):
        total += make_step(octos)
    return total


def flash_until_all(octos):
    """
    >>> octos = read_input('example')
    >>> flash_until_all(octos)
    195
    """
    n = 0
    while make_step(octos) != octos.size:
        n += 1
    return n + 1


if __name__ == "__main__":
    octos = read_input("input")
    print(count_flashes(octos, 100))
    octos = read_input("input")
    print(flash_until_all(octos))
