#!/usr/bin/env python

import re

mask_re = re.compile(r"mask = ([X01]+)")
mem_re = re.compile(r"mem\[(\d+)\] = (\d+)")

EX1 = [
    "mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X",
    "mem[8] = 11",
    "mem[7] = 101",
    "mem[8] = 0",
]


def parse_line(text):
    m = mask_re.match(text)
    if m:
        _or = int(m.group(1).replace("X", "0"), base=2)
        _and = int(m.group(1).replace("X", "1"), base=2)
        return (
            "MASK",
            {"or": _or, "and": _and},
        )
    m = mem_re.match(text)
    if m:
        return ("MEMSET", {"addr": int(m.group(1)), "value": int(m.group(2))})


def run_prog(code):
    """Meh
    >>> run_prog(EX1)
    165
    """
    mem = {}
    mask = None

    for line in code:
        op, args = parse_line(line)
        if op == "MASK":
            mask = args
        elif op == "MEMSET":
            mem[args["addr"]] = args["value"] & mask["and"] | mask["or"]

    return sum(mem.values())


if __name__ == "__main__":
    with open("input") as fd:
        lines = fd.readlines()
    print(run_prog(lines))
