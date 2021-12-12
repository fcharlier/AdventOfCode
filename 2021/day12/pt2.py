#!/usr/bin/python

import numpy as np


def read_input(filename):
    """
    >>> g = read_input('ex1')
    >>> len(g)
    5
    >>> g["start"]
    ['A', 'b']
    >>> g.get("end")
    >>> g.get("A")
    ['c', 'b', 'end']
    """
    g = {}
    with open(filename) as fd:
        for line in fd:
            a, b = line.strip().split("-")
            if a != "end" and b != "start":
                g[a] = g.get(a, []) + [b]
            if b != "end" and a != "start":
                g[b] = g.get(b, []) + [a]
    return g


def count_paths(g, start="start", seen=["start"]):
    """
    >>> count_paths(read_input('ex1'))
    36
    >>> count_paths(read_input('ex2'))
    103
    >>> count_paths(read_input('ex3'))
    3509
    """
    npaths = 0

    for nxt in g[start]:
        # print("     ", seen, "   =>  ", np.all(np.unique(seen, return_counts=True)[1] < 2))
        if nxt == "end":
            npaths += 1
            # print(f"{' - '.join(seen)} - end")
        elif (
            nxt.isupper()
            or nxt not in seen
            or nxt in seen and np.all(
                np.unique(np.char.asarray(seen)[np.char.asarray(seen).islower()], return_counts=True)[1] < 2
            )
        ):
            npaths += count_paths(g, nxt, seen + [nxt])
    return npaths


if __name__ == "__main__":
    print(count_paths(read_input("input")))
