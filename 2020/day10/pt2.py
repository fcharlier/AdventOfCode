#!/usr/bin/env python

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


def walk_and_gather(adapters):
    seen = dict(zip(adapters, [0] * len(adapters)))
    seen[0] = 1

    for n in adapters:
        if n + 1 in adapters:
            seen[n + 1] += seen[n]
        if n + 2 in adapters:
            seen[n + 2] += seen[n]
        if n + 3 in adapters:
            seen[n + 3] += seen[n]

    return seen[adapters[-1]]


def newends_OOM(adapters, ends):
    """Only works for small datasets like the examples"""
    while not all((val == adapters[-1] for val in ends)):
        result = []
        for val in ends:
            if val == adapters[-1]:
                result.append(val)
            else:
                for n in range(1, 4):
                    if val + n in adapters:
                        result.append(val + n)

        print(len(result))
        ends = result

    return len(ends)


def jolts_jumps_possibilities(adapters):
    """Meh
    >>> jolts_jumps_possibilities(tolist(EXAMPLE1))
    8
    >>> jolts_jumps_possibilities(tolist(EXAMPLE2))
    19208
    """

    adapters = (
        [0,] + sorted(adapters) + [max(adapters) + 3,]
    )

    return walk_and_gather(adapters)


if __name__ == "__main__":
    with open("input") as fd:
        adapters = tolist(fd.read())

    print(jolts_jumps_possibilities(adapters))
