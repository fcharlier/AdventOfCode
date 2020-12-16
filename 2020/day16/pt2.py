#!/usr/bin/env python


from functools import reduce
from operator import mul

EXAMPLE = """class: 0-1 or 4-19
row: 0-5 or 8-19
seat: 0-13 or 16-19

your ticket:
11,12,13

nearby tickets:
3,9,18
15,1,5
5,14,9
"""


def parse_input(text):
    """Meh
    >>> parse_input(EXAMPLE)
    ({'class': [(0, 1), (4, 19)], 'row': [(0, 5), (8, 19)], 'seat': [(0, 13), (16, 19)]}, [11, 12, 13], [[3, 9, 18], [15, 1, 5], [5, 14, 9]])
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
    >>> check_value(RULES, 11)
    True
    >>> check_value(RULES, 12)
    True
    >>> check_value(RULES, 13)
    True
    >>> check_value(RULES, 55)
    False
    >>> check_value(RULES, 83)
    False
    """
    return any((mi <= value <= ma for rule in rules.values() for mi, ma in rule))


def check_ticket(rules, ticket):
    return all(check_value(rules, val) for val in ticket)


def filter_tickets(rules, tickets):
    return [ticket for ticket in tickets if check_ticket(rules, ticket)]


def guess_valid_column(ranges, tickets):
    """
    >>> RULES, MINE, OTHERS = parse_input(EXAMPLE)
    >>> guess_valid_column(RULES['class'], filter_tickets(RULES, OTHERS))
    [1, 2]
    >>> guess_valid_column(RULES['row'], filter_tickets(RULES, OTHERS))
    [0, 1, 2]
    >>> guess_valid_column(RULES['seat'], filter_tickets(RULES, OTHERS))
    [2]
    """
    columns = list(zip(*tickets))
    ids = []
    for n, col in enumerate(columns):
        # print(all([any(mi <= value <= ma for mi, ma in ranges) for value in col]))
        if all([any(mi <= value <= ma for mi, ma in ranges) for value in col]):
            ids.append(n)
    return ids


if __name__ == "__main__":
    with open("input") as fd:
        rules, mine, tickets = parse_input(fd.read())
    tickets = filter_tickets(rules, tickets)

    valid_columns = {}
    for name, ranges in rules.items():
        valid_columns[name] = guess_valid_column(ranges, tickets)

    while not all((len(vs) == 1 for vs in valid_columns.values())):
        for name, vals in valid_columns.items():
            if len(vals) == 1:
                remove = vals[0]
                for k, v in valid_columns.items():
                    if k != name and remove in v:
                        v.remove(remove)

    departures = [
        mine[v[0]] for k, v in valid_columns.items() if k.startswith("departure")
    ]
    print(departures)
    print(reduce(mul, departures))
