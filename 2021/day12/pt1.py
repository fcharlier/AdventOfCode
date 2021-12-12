#!/usr/bin/python


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


def count_paths(g, start="start", seen=[]):
    """
    >>> count_paths(read_input('ex1'))
    10
    >>> count_paths(read_input('ex2'))
    19
    >>> count_paths(read_input('ex3'))
    226
    """
    npaths = 0

    for nxt in g[start]:
        # print(" " * len(seen) + f"{start} -> {nxt} : {seen}")
        if nxt == "end":
            npaths += 1
        elif nxt.isupper() or nxt not in seen:
            npaths += count_paths(g, nxt, seen + [nxt])
    return npaths


if __name__ == "__main__":
    print(count_paths(read_input("input")))
