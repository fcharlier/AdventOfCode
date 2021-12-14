#!/usr/bin/env python

from datetime import datetime
from collections import Counter


def read_input(filename):
    """
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


def template_to_pairs(template):
    """
    >>> template_to_pairs("NNCB")
    {'NN': 1, 'NC': 1, 'CB': 1}
    >>> template_to_pairs("NCNBCHB")
    {'NC': 1, 'CN': 1, 'NB': 1, 'BC': 1, 'CH': 1, 'HB': 1}
    >>> template_to_pairs("NBCCNBBBCBHCB")
    {'NB': 2, 'BC': 2, 'CC': 1, 'CN': 1, 'BB': 2, 'CB': 2, 'BH': 1, 'HC': 1}
    """
    pairs = {}
    for pair in [template[n : n + 2] for n in range(len(template) - 1)]:
        pairs[pair] = pairs.get(pair, 0) + 1
    return pairs


def polymer_char_counter(polymer, template):
    counter = Counter()
    for k, v in polymer.items():
        counter.update({k[0]: v})
    counter.update({template[-1]: 1})
    return counter.most_common()

def polymerize(template, rules, steps):
    """
    >>> template, rules = read_input('example')
    >>> polymerize(template, rules, 1) == template_to_pairs('NCNBCHB')
    True
    >>> polymerize(template, rules, 2) == template_to_pairs('NBCCNBBBCBHCB')
    True
    >>> polymerize(template, rules, 3) == template_to_pairs('NBBBCNCCNBBNBNBBCHBHHBCHB')
    True
    >>> polymerize(template, rules, 4) == template_to_pairs('NBBNBNBBCCNBCNCCNBBNBBNBBBNBBNBBCBHCBHHNHCBBCBHCB')
    True
    >>> sum(polymerize(template, rules, 5).values()) + 1
    97
    >>> res = polymerize(template, rules, 10)
    >>> sum(res.values()) + 1
    3073
    >>> polymer_char_counter(res, template)
    [('B', 1749), ('N', 865), ('C', 298), ('H', 161)]
    """
    pairs = template_to_pairs(template)

    for n in range(steps):
        new_pairs = {}
        for pair in pairs.keys():
            pl = pair[0] + rules[pair]
            pr = rules[pair] + pair[1]
            new_pairs[pl] = new_pairs.get(pl, 0) + pairs[pair]
            new_pairs[pr] = new_pairs.get(pr, 0) + pairs[pair]
        pairs = new_pairs

    return pairs


def polymer_value(counter):
    return counter[0][1] - counter[-1][1]


def main(filename, reps):
    """
    >>> main('example', 10)
    1588
    >>> main('example', 40)
    2188189693529
    """
    template, rules = read_input(filename)
    polymer = polymerize(template, rules, reps)
    counter = polymer_char_counter(polymer, template)
    return(polymer_value(counter))


if __name__ == "__main__":
    print(main("input", 40))
