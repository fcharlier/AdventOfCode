#!/usr/bin/env python

EXAMPLE = """939
7,13,x,x,59,x,31,19
"""

EX1 = """0
17,x,13,19
"""

EX2 = """0
67,7,59,61
"""

EX3 = """0
67,x,7,59,61
"""

EX4 = """0
67,7,x,59,61
"""

EX5 = """0
1789,37,47,1889
"""


def split_input(text):
    """Meh
    >>> split_input(EXAMPLE)
    [(0, 7), (1, 13), (4, 59), (6, 31), (7, 19)]
    """
    lines = text.strip().split()
    return list(
        (i, int(bline)) for i, bline in enumerate(lines[1].split(",")) if bline != "x"
    )


def meh(buslines):
    """Evaluate the truth statement for increasing amounts of bus lines, not resetting
    the timestamp after validating each amount.
    Recording the timestamp the test was valid for count `n` allows to increase the step
    when the test is valid again for count `n` during count `n+1` evaluation.
    >>> meh(split_input(EX1))
    3417
    >>> meh(split_input(EX2))
    754018
    >>> meh(split_input(EX3))
    779210
    >>> meh(split_input(EX4))
    1261476
    >>> meh(split_input(EX5))
    1202161486
    >>> meh(split_input(EXAMPLE))
    1068781
    """

    t = 0
    prevt = None
    step = buslines[0][1]

    for n in range(2, len(buslines) + 1):
        bls = buslines[:n]
        state = [(t + d) % b != 0 for d, b in bls]

        while any(state):
            t += step
            state = [(t + d) % b != 0 for d, b in bls]
            if prevt is not None and not any(state[:-2]):
                newstep = t - prevt
                step = newstep
                prevt = None  # Step change may happen only once per

        prevt = t

    return t


def earliest(buslines):
    """Once again, this works for the examples, but is far from optimal.
    >>> earliest(split_input(EX1))
    3417
    >>> earliest(split_input(EX2))
    754018
    >>> earliest(split_input(EX3))
    779210
    >>> earliest(split_input(EX4))
    1261476
    >>> earliest(split_input(EX5))
    1202161486
    >>> earliest(split_input(EXAMPLE))
    1068781
    """

    buslines.sort(key=lambda bl: bl[1], reverse=True)
    n = 0
    found = False
    while not found:
        n += 1
        t = buslines[0][1] * n - buslines[0][0]
        # print(t)

        stop = False
        for delta, busno in buslines:
            if (t + delta) % busno != 0:
                stop = False
                break
            else:
                stop = True

        if stop:
            found = True

    return t


if __name__ == "__main__":
    with open("input") as fd:
        # WAAAAY too slow for the final answer
        # print(earliest(split_input(fd.read())))
        print(meh(split_input(fd.read())))
