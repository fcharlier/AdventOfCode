#!/usr/bin/env python

import itertools
import re

mask_re = re.compile(r"mask = ([X01]+)")
mem_re = re.compile(r"mem\[(\d+)\] = (\d+)")

EX1 = [
    "mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X",
    "mem[8] = 11",
    "mem[7] = 101",
    "mem[8] = 0",
]


def apply_mask(mask, value):
    """
    >>> apply_mask("000000000000000000000000000000X1001X", 42)
    000000000000000000000000000000111010
    ['000000000000000000000000000000011010', '000000000000000000000000000000011011', '000000000000000000000000000000111010', '000000000000000000000000000000111011']
    >>> apply_mask("00000000000000000000000000000000X0XX", 26)
    000000000000000000000000000000011010
    ['000000000000000000000000000000010000', '000000000000000000000000000000010001', '000000000000000000000000000000010010', '000000000000000000000000000000010011', '000000000000000000000000000000011000', '000000000000000000000000000000011001', '000000000000000000000000000000011010', '000000000000000000000000000000011011']
    """
    bmask = int(mask.replace("X", "0"), base=2)
    sval = format(value | bmask, "036b")
    print(sval)
    nx = mask.count("X")
    rpl = list(itertools.product(("0", "1"), repeat=nx))
    result = [sval] * len(rpl)
    p = 0
    for m, r in enumerate(rpl):
        p = 0
        for c in r:
            p = mask.index("X", p)
            result[m] = result[m][:p] + c + result[m][p+1:]
            p += 1

    return result


def parse_line(text):
    m = mask_re.match(text)
    if m:
        return ("MASK", m.group(1))
    m = mem_re.match(text)
    if m:
        return ("MEMSET", {"addr": int(m.group(1)), "value": int(m.group(2))})


def run_prog(code):
    """Meh
    """
    mem = {}
    mask = None

    for line in code:
        op, args = parse_line(line)
        if op == "MASK":
            mask = args
        elif op == "MEMSET":
            for addr in apply_mask(mask, args["addr"]):
                mem[addr] = args["value"]

    return sum(mem.values())


if __name__ == "__main__":
    with open("input") as fd:
        lines = fd.readlines()
    print(run_prog(lines))
