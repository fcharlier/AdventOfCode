#!/usr/bin/env python

EXAMPLE = """0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

ababbb
bababa
abbbab
aaabbb
aaaabbb
"""


def parse_input(text):
    rules_txt, msgs_txt = text.strip().split("\n\n")

    rules = parse_rules(rules_txt)
    msgs = msgs_txt.strip().split()

    return rules, msgs


def parse_rules(rules_txt):
    """
    >>> rules = EXAMPLE.strip().split("\\n\\n")[0]
    >>> parse_rules(rules)
    {'0': [['4', '1', '5']], '1': [['2', '3'], ['3', '2']], '2': [['4', '4'], ['5', '5']], '3': [['4', '5'], ['5', '4']], '4': 'a', '5': 'b'}
    """
    rules = {}
    for rule_txt in rules_txt.strip().split("\n"):
        ruleno, constraints = rule_txt.split(":")

        if constraints.count('"') == 2:
            rules[ruleno] = constraints.strip().replace('"', "")
        else:
            rules[ruleno] = [c.strip().split() for c in constraints.split("|")]

    return rules


def match_rule(rules, ruleno, text, pos):
    """
    >>> rules, data = parse_input(EXAMPLE)
    >>> match_rule(rules, "0", data[0], 0)
    (True, 6)
    >>> match_rule(rules, "0", data[1], 0)
    (False, 6)
    >>> match_rule(rules, "0", data[2], 0)
    (True, 6)
    >>> match_rule(rules, "0", data[3], 0)
    (False, 6)
    >>> match_rule(rules, "0", data[4], 0)
    (True, 6)
    """

    if isinstance(rules[ruleno], str):
        res = text[pos] == rules[ruleno]
        return res, 1

    subm = []
    for subrs in rules[ruleno]:
        m = []
        d = 0
        for r in subrs:
            match, inc = match_rule(rules, r, text, pos + d)
            m.append(match)
            d += inc
        subm.append([all(m), d])
        if all(m):
            return True, d

    return False, d


def rule0(rules, text):
    """
    >>> rules, data = parse_input(EXAMPLE)
    >>> rule0(rules, data[0])
    True
    >>> rule0(rules, data[1])
    False
    >>> rule0(rules, data[2])
    True
    >>> rule0(rules, data[3])
    False
    >>> rule0(rules, data[4])
    False
    """
    mr = match_rule(rules, "0", text, 0)
    return mr[0] and mr[1] == len(text)


if __name__ == "__main__":
    with open("input") as fd:
        rules, data = parse_input(fd.read())
    res = [rule0(rules, text) for text in data]
    print(res.count(True))
