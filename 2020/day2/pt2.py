#!/usr/bin/env python

import re


def pwvalid(i1, i2, char, pw):
    """ Password Validation
    >>> pwvalid(1, 3, "a", "abcde")
    True
    >>> pwvalid(1, 3, "b", "cdefg")
    False
    >>> pwvalid(2, 9, "c", "ccccccccc")
    False
    """
    i1 = int(i1) - 1
    i2 = int(i2) - 1
    return (pw[i1] == char and pw[i2] != char) or (pw[i1] != char and pw[i2] == char)


if __name__ == "__main__":
    toCheck = []
    prog = re.compile(r"^(\d+)-(\d+) ([a-z]): ([a-z]+)$")
    with open("input") as fd:
        for line in fd.readlines():
            result = prog.match(line)
            toCheck.append(result.groups())
    print(len(list((True for pw in toCheck if pwvalid(*pw)))))
