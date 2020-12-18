#!/usr/bin/env python

import operator

EX1 = "1 + 2 * 3 + 4 * 5 + 6"
EX2 = "1 + (2 * 3) + (4 * (5 + 6))"
EX3 = "2 * 3 + (4 * 5)"
EX4 = "5 + (8 * 3 + 9 + 3 * 4 * 3)"
EX5 = "5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))"
EX6 = "((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2"


def eval_operand(expr, pos=0):
    """
    >>> eval_operand(EX1)
    (1, 1)
    >>> eval_operand(EX1[19:])
    (6, 2)
    >>> eval_operand(EX6)
    ('(2 + 4 * 9) * (6 + 9 * 8 + 6) + 6', 35)
    >>> eval_operand(EX6, 1)
    ('2 + 4 * 9', 12)
    >>> eval_operand("  36   ")
    (36, 4)
    >>>
    """
    while expr[pos] == " ":
        pos += 1
    start = pos

    if expr[pos] == "(":
        par_lvl = 1
        pos += 1
        while par_lvl:
            if expr[pos] == "(":
                par_lvl += 1
            elif expr[pos] == ")":
                par_lvl -= 1
            pos += 1

        return expr[start + 1 : pos - 1], pos
    else:
        while pos < len(expr) and expr[pos].isnumeric():
            pos += 1
        return int(expr[start:pos]), pos


def solve(expr, level=0):
    """Meh
    >>> solve(EX1)
    71
    >>> solve(EX2)
    51
    >>> solve(EX3)
    26
    >>> solve(EX4)
    437
    >>> solve(EX5)
    12240
    >>> solve(EX6)
    13632
    """

    if level > 100:
        return 0

    ops = {
        "+": operator.add,
        "*": operator.mul,
    }

    # Extract left operand
    left, pos = eval_operand(expr)

    if isinstance(left, str):
        left = solve(left)

    # Search & extract operator
    while expr[pos] not in ("+", "*"):
        pos += 1
    op = ops[expr[pos]]
    pos += 1

    # Extract right operand
    right, pos = eval_operand(expr, pos)

    if isinstance(right, str):
        right = solve(right)

    result = op(left, right)

    if pos < len(expr):
        result = solve(str(result) + expr[pos:], level + 1)

    return result


if __name__ == "__main__":
    with open("input") as fd:
        lines = fd.readlines()
    results = [solve(line.strip()) for line in lines]
    print(results)
    print(sum(results))
