#!/usr/bin/env python

EX1 = "1 + 2 * 3 + 4 * 5 + 6"
EX2 = "1 + (2 * 3) + (4 * (5 + 6))"
EX3 = "2 * 3 + (4 * 5)"
EX4 = "5 + (8 * 3 + 9 + 3 * 4 * 3)"
EX5 = "5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))"
EX6 = "((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2"


def eval_operand(expr, pos=0, direction=1):
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
    >>> eval_operand("123     ", 3, -1)
    (123, -1)
    >>> eval_operand(EX1, 9, -1)
    (3, 7)
    """
    while expr[pos] == " ":
        pos += direction
    start = pos

    if expr[pos] == "(":
        par_lvl = 1
        pos += direction
        while par_lvl:
            if expr[pos] == "(":
                par_lvl += 1
            elif expr[pos] == ")":
                par_lvl -= 1
            pos += 1
        res = expr[start + 1 : pos - 1]
        return res, pos
    else:
        while pos < len(expr) and pos >= 0 and expr[pos].isnumeric():
            pos += direction
        b = min(start, pos + 1)
        e = max(start + 1, pos)
        val = expr[b:e]
        res = int(val)

        return res, pos


def reduce_parens(expr):
    par_idx = expr.index("(")

    expr_left = expr[:par_idx]
    operand, pos = eval_operand(expr, par_idx)
    expr_right = expr[pos:]
    expr_paren = solve(operand) if isinstance(operand, str) else str(operand)

    return expr_left + str(expr_paren) + expr_right


def solve(expr, level=0):
    """Meh
    >>> solve("1 + 1")
    2
    >>> solve(EX1)
    231
    >>> solve("(1 + (1 + 1))")
    3
    >>> solve(EX2)
    51
    >>> solve(EX3)
    46
    >>> solve(EX4)
    1445
    >>> solve(EX5)
    669060
    >>> solve(EX6)
    23340
    """

    while "(" in expr:
        expr = reduce_parens(expr)

    while "+" in expr:
        idx = expr.index("+")
        left, posleft = eval_operand(expr, idx - 1, -1)
        right, posright = eval_operand(expr, idx + 1)
        center = left + right

        expr_l = expr[: posleft + 1]
        expr_r = expr[posright:]
        expr = expr_l + str(center) + expr_r

    while "*" in expr:
        idx = expr.index("*")
        left, posleft = eval_operand(expr, idx - 1, -1)
        right, posright = eval_operand(expr, idx + 1)
        center = left * right

        expr_l = expr[: posleft + 1]
        expr_r = expr[posright:]
        expr = expr_l + str(center) + expr_r

    return int(expr)


if __name__ == "__main__":
    with open("input") as fd:
        lines = fd.readlines()
    results = [solve(line.strip()) for line in lines]
    print(results)
    print(sum(results))
