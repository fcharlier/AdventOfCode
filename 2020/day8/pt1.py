#!/usr/bin/env python

TEST_PROG = """
nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6
"""


def parse_prog(lines):
    lines = lines.strip().split("\n")

    def parse_op(op, val):
        return (op, int(val))

    prog = [parse_op(*line.strip().split()) for line in lines]
    return prog


def run_prog(prog):
    """Meh
    >>> run_prog(parse_prog(TEST_PROG))
    5
    """
    accumulator = 0
    cur_op = 0
    seen_ops = []

    n = 1
    while cur_op not in seen_ops:
        seen_ops.append(cur_op)
        if prog[cur_op][0] == "nop":
            # print(n, cur_op, "nop")
            cur_op += 1
        elif prog[cur_op][0] == "acc":
            accumulator += prog[cur_op][1]
            # print(n, cur_op, "acc", prog[cur_op][1], "=>", accumulator)
            cur_op += 1
        elif prog[cur_op][0] == "jmp":
            # print(n, cur_op, "jmp", prog[cur_op][1])
            cur_op += prog[cur_op][1]
        n += 1

    return accumulator


if __name__ == "__main__":
    with open("input") as fd:
        prog_input = fd.read()
    print(run_prog(parse_prog(prog_input)))
