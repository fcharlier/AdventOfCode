#!/usr/bin/env python

import operator

EXAMPLE1 = """16
10
15
5
1
11
7
19
6
12
4
"""

EXAMPLE2 = """28
33
18
42
31
14
46
20
48
47
24
23
49
45
19
38
39
11
1
32
25
35
8
17
7
9
4
2
34
10
3
"""


def tolist(text):
    return [int(line) for line in text.strip().split()]


def jolts_jumps(adapters):
    """Meh
    >>> jolts_jumps(tolist(EXAMPLE1))
    [1, 3, 1, 1, 1, 3, 1, 1, 3, 1, 3, 3]
    """
    adapters = (
        [0,] + sorted(adapters) + [max(adapters) + 3,]
    )
    return [n - adapters[i - 1] for i, n in list(enumerate(adapters))[1:]]


def jolts_jumps_buckets(jumps):
    """Meh
    >>> jolts_jumps_buckets(jolts_jumps(tolist(EXAMPLE1)))
    {1: 7, 3: 5}
    >>> jolts_jumps_buckets(jolts_jumps(tolist(EXAMPLE2)))
    {1: 22, 3: 10}
    """
    return {jump: jumps.count(jump) for jump in set(jumps)}


if __name__ == "__main__":
    with open("input") as fd:
        adapters = tolist(fd.read())

    buckets = jolts_jumps_buckets(jolts_jumps(adapters))
    print(buckets[1] * buckets[3])
