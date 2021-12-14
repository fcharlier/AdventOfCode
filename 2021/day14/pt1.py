#!/usr/bin/env python

from datetime import datetime
from collections import Counter


def read_input(filename):
    """Meh
    >>> template, ins_rules = read_input('example')
    >>> template
    'NNCB'
    >>> len(ins_rules)
    16
    >>> ins_rules['NH']
    'C'
    >>> ins_rules['BH']
    'H'
    """
    template = ""
    ins_rules = {}
    with open(filename) as fd:
        for line in fd:
            line = line.strip()
            if " -> " in line:
                a, b = line.split(" -> ")
                ins_rules[a] = b
            elif len(line):
                template = line
    return template, ins_rules


def polymerization_step(template, rules):
    """
    >>> template, rules = read_input('example')
    >>> template
    'NNCB'
    >>> template = polymerization_step(template, rules)
    >>> template
    'NCNBCHB'
    >>> template = polymerization_step(template, rules)
    >>> template
    'NBCCNBBBCBHCB'
    >>> template = polymerization_step(template, rules)
    >>> template
    'NBBBCNCCNBBNBNBBCHBHHBCHB'
    >>> template = polymerization_step(template, rules)
    >>> template
    'NBBNBNBBCCNBCNCCNBBNBBNBBBNBBNBBCBHCBHHNHCBBCBHCB'
    """
    for n in range(0, len(template) * 2 - 2, 2):
        template = template[0 : n + 1] + rules[template[n : n + 2]] + template[n + 1 :]
    return template


def polymerize(template, rules, steps):
    """
    >>> template, rules = read_input('example')
    >>> polymer = polymerize(template, rules, 5)
    >>> len(polymer)
    97
    >>> polymer = polymerize(template, rules, 10)
    >>> len(polymer)
    3073
    >>> freqs = Counter(polymer)
    >>> freqs["B"]
    1749
    >>> freqs["C"]
    298
    >>> freqs["H"]
    161
    >>> freqs["N"]
    865
    """
    polymer = template
    for n in range(steps):
        polymer = polymerization_step(polymer, rules)
    return polymer


def polymer_value(polymer):
    """
    >>> polymer = polymerize(*read_input('example'), 10)
    >>> polymer_value(polymer)
    1588
    """
    freqs = Counter(polymer).most_common()
    return freqs[0][1] - freqs[-1][1]


if __name__ == "__main__":
    print(polymer_value(polymerize(*read_input("input"), 10)))
