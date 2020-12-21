#!/usr/bin/env python

EXAMPLE = """42: 9 14 | 10 1
9: 14 27 | 1 26
10: 23 14 | 28 1
1: "a"
11: 42 31
5: 1 14 | 15 1
19: 14 1 | 14 14
12: 24 14 | 19 1
16: 15 1 | 14 14
31: 14 17 | 1 13
6: 14 14 | 1 14
2: 1 24 | 14 4
0: 8 11
13: 14 3 | 1 12
15: 1 | 14
17: 14 2 | 1 7
23: 25 1 | 22 14
28: 16 1
4: 1 1
20: 14 14 | 1 15
3: 5 14 | 16 1
27: 1 6 | 14 18
14: "b"
21: 14 1 | 1 14
25: 1 1 | 1 14
22: 14 14
8: 42
26: 14 22 | 1 20
18: 15 15
7: 14 5 | 1 21
24: 14 1

abbbbbabbbaaaababbaabbbbabababbbabbbbbbabaaaa
bbabbbbaabaabba
babbbbaabbbbbabbbbbbaabaaabaaa
aaabbbbbbaaaabaababaabababbabaaabbababababaaa
bbbbbbbaaaabbbbaaabbabaaa
bbbababbbbaaaaaaaabbababaaababaabab
ababaaaaaabaaab
ababaaaaabbbaba
baabbaaaabbaaaababbaababb
abbbbabbbbaaaababbbbbbaaaababb
aaaaabbaabaaaaababaa
aaaabbaaaabbaaa
aaaabbaabbaaaaaaabbbabbbaaabbaabaaa
babaaabbbaaabaababbaabababaaab
aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba
"""


def parse_input(text):
    rules_txt, msgs_txt = text.strip().split("\n\n")

    rules = parse_rules(rules_txt)
    msgs = msgs_txt.strip().split()

    return rules, msgs


def parse_rules(rules_txt):
    rules = {}
    for rule_txt in rules_txt.strip().split("\n"):
        ruleno, constraints = rule_txt.split(":")

        if constraints.count('"') == 2:
            rules[ruleno] = constraints.strip().replace('"', "")
        else:
            rules[ruleno] = [c.strip().split() for c in constraints.split("|")]

    return rules


def match_rule(rules, ruleno, text, pos, rec=0):
    # """
    # >>> rules, data = parse_input(EXAMPLE)
    # >>> match_rule(rules, "0", "bbabbbbaabaabba", 0)
    # (True, 15)
    # >>> match_rule(rules, "0", "ababaaaaaabaaab", 0)
    # (True, 15)
    # >>> match_rule(rules, "0", "ababaaaaabbbaba", 0)
    # (True, 15)
    # >>> match_rule(rules, "42", "bbabbbbaabaabba", 0)
    # (True, 5)
    # >>> match_rule(rules, "42", "bbabbbbaabaabba", 5)
    # (True, 5)
    # >>> match_rule(rules, "31", "bbabbbbaabaabba", 10)
    # (True, 5)
    # """
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

    return False, 0


def rule_42_42_31(rules, text):
    """ We changed rules 8 and 11 which are now recursive.
    However, the problem sould be veirified onlu for our specific set of rules.
    We can see that rule 0 is: 8 11 (oh, our two rules …)
    8 is: 42 | 42 8, reduced to one or more times rule 42
    11 is: 42 31 | 42 11 31, reduced to one or more times 42 and as many times 31
    That's all we need to solve for now, match rule 42 as much as we can and verify that
    we can match rule 31 at lease one more time.

    I've struggled a lot with this one trying to make it work with a "generic" algorithm
    and then struggling again with index errors for this solution which I don't like at
    all.
    >>> rules, data = parse_input(EXAMPLE)
    >>> rule_42_42_31(rules, "bbabbbbaabaabba")
    True
    >>> rule_42_42_31(rules, "babbbbaabbbbbabbbbbbaabaaabaaa")
    True
    >>> rule_42_42_31(rules, "aaabbbbbbaaaabaababaabababbabaaabbababababaaa")
    True
    >>> rule_42_42_31(rules, "bbbbbbbaaaabbbbaaabbabaaa")
    True
    >>> rule_42_42_31(rules, "bbbababbbbaaaaaaaabbababaaababaabab")
    True
    >>> rule_42_42_31(rules, "ababaaaaaabaaab")
    True
    >>> rule_42_42_31(rules, "ababaaaaabbbaba")
    True
    >>> rule_42_42_31(rules, "baabbaaaabbaaaababbaababb")
    True
    >>> rule_42_42_31(rules, "abbbbabbbbaaaababbbbbbaaaababb")
    True
    >>> rule_42_42_31(rules, "aaaaabbaabaaaaababaa")
    True
    >>> rule_42_42_31(rules, "aaaabbaabbaaaaaaabbbabbbaaabbaabaaa")
    True
    >>> rule_42_42_31(rules, "aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba")
    True
    """

    pos = 0
    matches_42 = 0
    matches_31 = 0
    try:
        m, d = match_rule(rules, "42", text, 0)
        m31 = False
        while m and pos < len(text) and not m31:
            try:
                pos += d
                matches_42 += 1
                m, d = match_rule(rules, "42", text, pos)
                m31, _ = match_rule(rules, "31", text, pos)
            except IndexError:
                pass

        if m31:
            pos -= d

        m, d = match_rule(rules, "31", text, pos)
        while m and pos < len(text):
            try:
                pos += d
                matches_31 += 1
                m, d = match_rule(rules, "31", text, pos)
            except IndexError:
                pass
    except IndexError:
        pass

    if matches_42 > matches_31 > 0 and pos == len(text):
        return True
    else:
        return False


if __name__ == "__main__":
    with open("input2") as fd:
        rules, data = parse_input(fd.read())
    res = [rule_42_42_31(rules, text) for text in data]
    print(res.count(True))
