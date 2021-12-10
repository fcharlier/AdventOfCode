#!/usr/bin/env python


def read_input(filename):
    with open(filename) as fd:
        return [line.strip() for line in fd.readlines()]


def reduce_chunks(line):
    """Meh
    >>> lines = read_input('example')
    >>> reduce_chunks(lines[2])
    '{([(<[}>{{[('
    """
    while True:
        prev = line
        for crs in ("()", "[]", "{}", "<>"):
            line = line.replace(crs, "")
        if prev == line:
            return line


def first_bad(line):
    """Meh
    >>> lines = read_input('example')
    >>> first_bad(lines[0])
    ''
    >>> first_bad(lines[2])
    '}'
    >>> first_bad(lines[4])
    ')'
    >>> first_bad(lines[5])
    ']'
    >>> first_bad(lines[7])
    ')'
    >>> first_bad(lines[8])
    '>'
    """
    line = reduce_chunks(line)
    for crs in ("(", "[", "{", "<"):
        line = line.replace(crs, "")
    if len(line):
        return line[0]
    return ""


def syntax_score(lines):
    """
    >>> syntax_score(read_input('example'))
    26397
    """
    badchrs = [first_bad(line) for line in lines]
    chrvals = {"": 0, ")": 3, "]": 57, "}": 1197, ">": 25137}
    score = 0
    for char in chrvals.keys():
        score += badchrs.count(char) * chrvals[char]
    return score


def filter_incomplete_lines(lines):
    """
    >>> len(filter_incomplete_lines(read_input('example')))
    5
    """
    return [reduce_chunks(line) for line in lines if first_bad(line) == ""]


def incomplete_score(line):
    """
    >>> lines = filter_incomplete_lines(read_input('example'))
    >>> incomplete_score(lines[0])
    288957
    >>> incomplete_score(lines[1])
    5566
    >>> incomplete_score(lines[2])
    1480781
    >>> incomplete_score(lines[3])
    995444
    >>> incomplete_score(lines[4])
    294
    """
    chrvals = {"(": 1, "[": 2, "{": 3, "<": 4}
    score = 0
    for char in line[::-1]:
        score = score * 5 + chrvals[char]
    return score


def final_incomplete_score(lines):
    """
    >>> lines = filter_incomplete_lines(read_input('example'))
    >>> final_incomplete_score(lines)
    288957
    """
    scores = [incomplete_score(line) for line in lines]
    return sorted(scores)[len(scores) // 2]


if __name__ == "__main__":
    lines = read_input("input")
    print(syntax_score(lines))
    print(final_incomplete_score(filter_incomplete_lines(lines)))
