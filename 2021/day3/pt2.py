#!/usr/bin/env python

""" Meh
"""

EX_INPUT = """00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010
"""


def most_common(column):
    """
    >>> most_common(["0", "0", "1"])
    '0'
    >>> most_common(["1", "1", "0", "0", "1"])
    '1'
    """
    occurs = {}
    for bit in column:
        occurs[bit] = occurs.get(bit, 0) + 1
    if occurs["0"] == occurs["1"]:
        return "1"
    return max(occurs, key=lambda v: occurs[v])


def least_common(column):
    """
    >>> least_common(["0", "0", "1"])
    '1'
    >>> least_common(["1", "1", "0", "0", "1"])
    '0'
    """
    occurs = {}
    for bit in column:
        occurs[bit] = occurs.get(bit, 0) + 1
    if occurs["0"] == occurs["1"]:
        return "0"
    return min(occurs, key=lambda v: occurs[v])


def load_report(report):
    """Splits the report from a string into a list of list of "bits" """
    return [list(c for c in code) for code in report.split("\n") if len(code)]


def transpose_report(report):
    """Transposes the report. Columns into rows"""
    return list(map(list, zip(*report)))


def oxygen_rating(report):
    """ O2 Rating
    >>> report = load_report(EX_INPUT)
    >>> oxygen_rating(report)
    23
    """
    col = 0
    while len(report) > 1:
        mcom = most_common(transpose_report(report)[col])
        report = [row for row in report if row[col] == mcom]
        col += 1
    return int("".join(report[0]), 2)


def co2_rating(report):
    """ CO2 Rating
    >>> report = load_report(EX_INPUT)
    >>> co2_rating(report)
    10
    """
    col = 0
    while len(report) > 1:
        lcom = least_common(transpose_report(report)[col])
        report = [row for row in report if row[col] == lcom]
        col += 1
    return int("".join(report[0]), 2)


if __name__ == "__main__":
    with open("input") as report_file:
        rpt = load_report(report_file.read())
    o2r = oxygen_rating(rpt)
    co2r = co2_rating(rpt)
    print(o2r, co2r, o2r * co2r)
