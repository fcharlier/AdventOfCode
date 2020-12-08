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


def run_modify_prog(prog):
    """Meh
    >>> run_modify_prog(parse_prog(TEST_PROG))
    8
    """
    change_op = 0
    cur_op = 0

    while cur_op < len(prog) and change_op < len(prog):
        accumulator = 0
        cur_op = 0
        seen_ops = []

        while cur_op not in seen_ops and cur_op < len(prog):
            op, val = prog[cur_op]
            if cur_op == change_op:
                if op == "jmp":
                    op = "nop"
                elif op == "nop":
                    op = "jmp"

            seen_ops.append(cur_op)
            if op == "nop":
                cur_op += 1
            elif op == "acc":
                accumulator += val
                cur_op += 1
            elif op == "jmp":
                cur_op += val

        change_op += 1

    if cur_op == len(prog):
        return accumulator
    else:
        return None


if __name__ == "__main__":
    with open("input") as fd:
        prog_input = fd.read()
    print(run_modify_prog(parse_prog(prog_input)))
