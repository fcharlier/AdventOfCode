#!/usr/bin/env python


def count_increases(report):
    """Meh
    >>> count_increases([199, 200, 208, 210, 200, 207, 240, 269, 260, 263])
    7
    """
    return sum((1 if report[n] < report[n + 1] else 0 for n in range(len(report) - 1)))


def sliding_sum(report):
    """Meh
    >>> sliding_sum([199, 200, 208, 210, 200, 207, 240, 269, 260, 263])
    [607, 618, 618, 617, 647, 716, 769, 792]
    """
    return [sum(report[n : n + 3]) for n in range(len(report) - 2)]


if __name__ == "__main__":
    with open("input") as data:
        report = [int(n.strip()) for n in data.readlines()]
    print(count_increases(report))
    print(count_increases(sliding_sum(report)))
