#!/usr/bin/python3

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


def do_op(item, op):
    o1 = item if op[0] == "old" else int(op[0])
    o2 = item if op[2] == "old" else int(op[2])
    OP = {
        "+": add,
        "*": mul,
    }

    result = OP[op[1]](o1, o2)
    third = result // 3
    # print(f"{op} => {result} => {third}")
    return third


def play_round(monkeys):
    for monkey in monkeys.values():
        for item in monkey["items"]:
            item = do_op(item, monkey["op"])
            if item % monkey["test"] == 0:
                target = monkey["true"]
            else:
                target = monkey["false"]
            # print(f"Pass {item} to monkey {target}.")
            monkeys[target]["items"].append(item)
            monkey["inspections"] += 1
        monkey["items"] = []


def monkey_business_level(monkeys):
    inspections = sorted(monkey["inspections"] for monkey in monkeys.values())[-2:]
    return mul(*inspections)


def play(monkeys, rounds=20):
    """
    >>> monkeys = parse_input("input_example")
    >>> play(monkeys, 1)
    >>> monkeys[0]["items"]
    [20, 23, 27, 26]
    >>> monkeys[1]["items"]
    [2080, 25, 167, 207, 401, 1046]
    >>> monkeys[2]["items"]
    []
    >>> monkeys[3]["items"]
    []
    >>> play(monkeys, 1)
    >>> monkeys[0]["items"]
    [695, 10, 71, 135, 350]
    >>> monkeys[1]["items"]
    [43, 49, 58, 55, 362]
    >>> monkeys[2]["items"]
    []
    >>> monkeys[3]["items"]
    []
    >>> play(monkeys, 18)
    >>> monkeys[0]["items"]
    [10, 12, 14, 26, 34]
    >>> monkeys[1]["items"]
    [245, 93, 53, 199, 115]
    >>> monkeys[2]["items"]
    []
    >>> monkeys[3]["items"]
    []
    >>> monkeys[0]["inspections"]
    101
    >>> monkeys[1]["inspections"]
    95
    >>> monkeys[2]["inspections"]
    7
    >>> monkeys[3]["inspections"]
    105
    >>> monkey_business_level(monkeys)
    10605
    """
    for _ in range(rounds):
        play_round(monkeys)


if __name__ == "__main__":
    monkeys = parse_input("input_real")
    play(monkeys, 20)
    print(monkey_business_level(monkeys))
