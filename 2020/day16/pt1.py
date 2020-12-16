#!/usr/bin/env python

EXAMPLE = """class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12
"""


def parse_input(text):
    """Meh
    >>> parse_input(EXAMPLE)
    ({'class': [(1, 3), (5, 7)], 'row': [(6, 11), (33, 44)], 'seat': [(13, 40), (45, 50)]}, [7, 1, 14], [[7, 3, 47], [40, 4, 50], [55, 2, 20], [38, 6, 12]])
    """
    rules = {}
    myticket = []
    nearbytickets = []
    mode = "rules"
    for line in text.strip().split("\n"):
        if line == "":
            continue
        if line.startswith("your ticket:"):
            mode = "myticket"
            continue
        if line.startswith("nearby tickets:"):
            mode = "nearby"
            continue

        if mode == "rules":
            rulename, constraints = line.split(":")
            constraints = constraints.split(" or ")
            ranges = [tuple(map(int, rng.strip().split("-"))) for rng in constraints]
            rules[rulename] = ranges
            continue

        if mode in ("myticket", "nearby"):
            ticket = [int(n) for n in line.strip().split(",")]
            if mode == "myticket":
                myticket = ticket
                continue

            if mode == "nearby":
                nearbytickets.append(ticket)
                continue

    return rules, myticket, nearbytickets


def check_value(rules, value):
    """
    >>> RULES = parse_input(EXAMPLE)[0]
    >>> check_value(RULES, 7)
    True
    >>> check_value(RULES, 1)
    True
    >>> check_value(RULES, 14)
    True
    >>> check_value(RULES, 40)
    True
    >>> check_value(RULES, 50)
    True
    >>> check_value(RULES, 38)
    True
    >>> check_value(RULES, 4)
    False
    >>> check_value(RULES, 55)
    False
    >>> check_value(RULES, 12)
    False
    """
    return any((mi <= value <= ma for rule in rules.values() for mi, ma in rule))


def process_tickets(rules, mine, others):
    """
    >>> process_tickets(*parse_input(EXAMPLE))
    [4, 55, 12]
    """
    invalid_values = []

    invalid_values.extend((value for value in mine if not check_value(rules, value)))

    for ticket in others:
        invalid_values.extend(
            (value for value in ticket if not check_value(rules, value))
        )

    return invalid_values


if __name__ == "__main__":
    with open("input") as fd:
        print(sum(process_tickets(*parse_input(fd.read()))))
