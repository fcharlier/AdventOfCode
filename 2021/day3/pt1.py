#!/usr/bin/env python

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
    return min(occurs, key=lambda v: occurs[v])


def transpose_report(report):
    """ Splits & transposes the report
    """
    l_o_l = [list(c for c in code) for code in report.split("\n") if len(code)]
    return list(map(list, zip(*l_o_l)))


def gamma_rate(report):
    """Meh
    >>> report = transpose_report(EX_INPUT)
    >>> gamma_rate(report)
    22
    """
    rate = ""

    for col in report:
        mcom = most_common(col)
        rate += mcom

    return int(rate, 2)


def epsilon_rate(report):
    """
    >>> report = transpose_report(EX_INPUT)
    >>> epsilon_rate(report)
    9
    """
    rate = ""

    for col in report:
        lcom = least_common(col)
        rate += lcom

    return int(rate, 2)


if __name__ == "__main__":
    with open("input") as report_file:
        rpt = transpose_report(report_file.read())
    g_rate = gamma_rate(rpt)
    e_rate = epsilon_rate(rpt)
    print(g_rate, e_rate, g_rate * e_rate)
