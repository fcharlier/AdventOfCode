#!/usr/bin/python3

from operator import truth


def is_okay(num):
    sn = str(num)
    has_double = False

    for n in range(len(sn) - 1):
        if sn[n] > sn[n + 1]:
            return False
        has_double = has_double or sn[n] == sn[n + 1]
    return has_double


print(len(list(filter(truth, map(is_okay, range(197487, 673251))))))
