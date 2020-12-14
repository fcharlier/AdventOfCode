#!/usr/bin/env python

EXAMPLE = """939
7,13,x,x,59,x,31,19
"""


def split_input(text):
    """Meh
    >>> split_input(EXAMPLE)
    (939, [7, 13, 59, 31, 19])
    """
    lines = text.strip().split()
    return int(lines[0]), [int(bline) for bline in lines[1].split(",") if bline != "x"]


def earliest(timestamp, buslines):
    """Meh
    >>> earliest(*split_input(EXAMPLE))
    [59, 944]
    295
    """
    earliest_per_line = [
        [busno, (timestamp // busno + 1) * busno] for busno in buslines
    ]
    earliest_line = min(earliest_per_line, key=lambda e: e[1])
    print(earliest_line)
    return earliest_line[0] * (earliest_line[1] - timestamp)


if __name__ == "__main__":
    with open("input") as fd:
        print(earliest(*split_input(fd.read())))
