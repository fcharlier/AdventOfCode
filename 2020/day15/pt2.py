#!/usr/bin/env python

from datetime import datetime
import sys


def speak_numbers(initial, count):
    """As expected, initial algo from part1 is too slow & memory hungry.
    This one is better, storing only the seen numbers & their latest seen index.
    >>> speak_numbers(np.array([0, 3, 6]), 10)
    0
    >>> speak_numbers(np.array([1, 3, 2]), 2020)
    1
    >>> speak_numbers(np.array([2, 1, 3]), 2020)
    10
    >>> speak_numbers(np.array([1, 2, 3]), 2020)
    27
    >>> speak_numbers(np.array([2, 3, 1]), 2020)
    78
    >>> speak_numbers(np.array([3, 2, 1]), 2020)
    438
    >>> speak_numbers(np.array([3, 1, 2]), 2020)
    1836
    >>> speak_numbers(np.array([0, 3, 6]), 30000000)
    175594
    >>> speak_numbers(np.array([1, 3, 2]), 30000000)
    2578
    >>> speak_numbers(np.array([2, 1, 3]), 30000000)
    3544142
    >>> speak_numbers(np.array([1, 2, 3]), 30000000)
    261214
    >>> speak_numbers(np.array([2, 3, 1]), 30000000)
    6895259
    >>> speak_numbers(np.array([3, 2, 1]), 30000000)
    18
    >>> speak_numbers(np.array([3, 1, 2]), 30000000)
    362
    """
    seen = dict(zip(initial[:-1], range(1, len(initial[:-1]) + 1)))
    nextnum = initial[-1]
    for n in range(len(initial) + 1, count + 1):
        search = nextnum
        last_seen = seen.get(search)
        seen[search] = n - 1
        if last_seen:
            nextnum = n - 1 - last_seen
        else:
            nextnum = 0

    return nextnum


if __name__ == "__main__":
    with open("input") as fd:
        initial = [int(n.strip()) for n in fd.read().strip().split(",")]

    print(sys.version)

    print("Part 1, 2020 iterations:")
    tstart = datetime.now()
    print("    ", speak_numbers(initial, 2020))
    tend = datetime.now()
    print("  Took:", (tend - tstart).total_seconds(), "seconds")

    print("Part 2, 30000000 iterations:")
    tstart = datetime.now()
    print("    ", speak_numbers(initial, 30000000))
    tend = datetime.now()
    print("  Took:", (tend - tstart).total_seconds(), "seconds")
