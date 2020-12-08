#!/usr/bin/env python

import re


def pwvalid(minCount, maxCount, char, pw):
    """ Password Validation
    >>> pwvalid(1, 3, "a", "abcde")
    True
    >>> pwvalid(1, 3, "b", "cdefg")
    False
    >>> pwvalid(2, 9, "c", "ccccccccc")
    True
    """
    return int(minCount) <= pw.count(char) <= int(maxCount)


if __name__ == "__main__":
    toCheck = []
    prog = re.compile(r"^(\d+)-(\d+) ([a-z]): ([a-z]+)$")
    with open("input") as fd:
        for line in fd.readlines():
            result = prog.match(line)
            toCheck.append(result.groups())
    print(len(list((True for pw in toCheck if pwvalid(*pw)))))
