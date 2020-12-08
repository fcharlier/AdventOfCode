#!/usr/bin/python3

from operator import truth


def is_okay(num):
    sn = str(num)
    doubles = [0] * 10

    for n in range(len(sn) - 1):
        if sn[n] > sn[n + 1]:
            return False
        if sn[n] == sn[n + 1]:
            doubles[int(sn[n])] += 1
    return len([n for n in doubles if n == 1])


print(len(list(filter(truth, map(is_okay, range(197487, 673251))))))
