#!/usr/bin/env python

from itertools import product
import functools

"""
Didn't know about @functools.cache, found by looking at r/adventofcode talking about
memoize & @functools.cache.

Helps, else resolution time might be veeeery long & RAM hungry.
"""


def throw_dice():
    return product(range(1, 4), range(1, 4), range(1, 4))


dices = [sum(d) for d in throw_dice()]


@functools.cache
def play_dice(posp1, posp2, scorep1=0, scorep2=0, turn=0):
    """
    >>> play_dice(4 - 1, 8 - 1, 0, 0)
    [444356092776315, 341960390180808]
    """
    wins = [0, 0]

    if scorep1 >= 21:
        return (1, 0)
    if scorep2 >= 21:
        return (0, 1)

    for throw in dices:
        nextpos = [posp1, posp2]
        nextscores = [scorep1, scorep2]

        player = turn % 2

        nextpos[player] = (nextpos[player] + throw) % 10
        nextscores[player] += nextpos[player] + 1
        result = play_dice(*nextpos, *nextscores, turn + 1)
        wins = [result[n] + wins[n] for n in range(2)]
    return wins


if __name__ == "__main__":
    print(max(play_dice(6 - 1, 9 - 1)))
