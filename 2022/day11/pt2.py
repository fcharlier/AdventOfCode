#!/usr/bin/python3

from functools import reduce
from operator import add, mul
import re


def add_monkey(monkeys, num):
    """Just create an empty monkey"""
    monkeys[num] = {
        "inspections": 0,
        "items": [],
        "op": None,
        "test": None,
        "true": None,
        "false": None,
    }


def parse_input(filename):
    """Reads into structure
    >>> monkeys = parse_input("input_example")
    >>> len(monkeys)
    4
    >>> monkeys[1]["items"]
    [54, 65, 75, 74]
    >>> monkeys[1]["op"]
    ('old', '+', '6')
    >>> monkeys[1]["test"]
    19
    >>> monkeys[1]["true"]
    2
    >>> monkeys[1]["false"]
    0
    """
    monkeys = {}
    with open(filename) as fd:
        for line in fd:
            if m := re.search(r"Monkey (\d+):", line):
                monkey_no = int(m.group(1))
                add_monkey(monkeys, monkey_no)
            elif m := re.search(r"Starting items: (\d+.*)+", line):
                monkeys[monkey_no]["items"] = list(map(int, m.group(1).split(", ")))
            elif m := re.search(r"Operation: new = (\S+) ([+*]) (\S+)", line):
                monkeys[monkey_no]["op"] = (m.group(1), m.group(2), m.group(3))
            elif m := re.search(r"Test: divisible by (\d+)", line):
                monkeys[monkey_no]["test"] = int(m.group(1))
            elif m := re.search(r"If (true|false): throw to monkey (\d+)", line):
                monkeys[monkey_no][m.group(1)] = int(m.group(2))
    return monkeys


def do_op(item, op, relief_divisor):
    o1 = item if op[0] == "old" else int(op[0])
    o2 = item if op[2] == "old" else int(op[2])
    OP = {
        "+": add,
        "*": mul,
    }

    result = OP[op[1]](o1, o2)
    third = result % relief_divisor
    return third


def play_round(monkeys, relief_divisor):
    for monkey in monkeys.values():
        for item in monkey["items"]:
            item = do_op(item, monkey["op"], relief_divisor)
            if item % monkey["test"] == 0:
                target = monkey["true"]
            else:
                target = monkey["false"]
            monkeys[target]["items"].append(item)
            monkey["inspections"] += 1
        monkey["items"] = []


def monkey_business_level(monkeys):
    inspections = sorted(monkey["inspections"] for monkey in monkeys.values())[-2:]
    return mul(*inspections)


def play(monkeys, rounds=20, relief_divisor=3):
    """
    >>> monkeys = parse_input("input_example")
    >>> divisor = reduce(mul, (monkey["test"] for monkey in monkeys.values()))
    >>> play(monkeys, 1, relief_divisor=divisor)
    >>> monkeys[0]["inspections"]
    2
    >>> monkeys[1]["inspections"]
    4
    >>> monkeys[2]["inspections"]
    3
    >>> monkeys[3]["inspections"]
    6
    >>> play(monkeys, 19, relief_divisor=divisor)
    >>> monkeys[0]["inspections"]
    99
    >>> monkeys[1]["inspections"]
    97
    >>> monkeys[2]["inspections"]
    8
    >>> monkeys[3]["inspections"]
    103
    >>> monkeys = parse_input("input_example")
    >>> divisor = reduce(mul, (monkey["test"] for monkey in monkeys.values()))
    >>> play(monkeys, 10000, relief_divisor=divisor)
    >>> monkey_business_level(monkeys)
    2713310158
    """
    for n in range(rounds):
        play_round(monkeys, relief_divisor)


if __name__ == "__main__":
    monkeys = parse_input("input_real")
    # Hint from https://github.com/sdatko/advent-of-code/blob/master/year-2022/day-11/part-2.py
    # Due to division, modulo etc. only have to handle values modulo common divisor,
    # which is the multiplication of each monkey's test value
    # And we don't really care about the exact values but only if they're divisible by
    # each monkey's "test"
    divisor = reduce(mul, (monkey["test"] for monkey in monkeys.values()))
    play(monkeys, 10000, divisor)
    print(monkey_business_level(monkeys))
