#!/usr/bin/env python

import re
import itertools

TEST_RULES_TEXT = """light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags."""
TEST_RULES = TEST_RULES_TEXT.split("\n")

bag_re = re.compile(r"(?P<color>\w+ \w+) bags contain")
content_re = re.compile(r"(?P<count>\d+) (?P<color>\w+ \w+) bags?")


def rule_to_python(rule):
    """Meh
    >>> rule_to_python(TEST_RULES[0])
    {'light red': {'bright white': 1, 'muted yellow': 2}}
    >>> rule_to_python(TEST_RULES[1])
    {'dark orange': {'bright white': 3, 'muted yellow': 4}}
    >>> rule_to_python(TEST_RULES[2])
    {'bright white': {'shiny gold': 1}}
    >>> rule_to_python(TEST_RULES[3])
    {'muted yellow': {'shiny gold': 2, 'faded blue': 9}}
    >>> rule_to_python(TEST_RULES[4])
    {'shiny gold': {'dark olive': 1, 'vibrant plum': 2}}
    >>> rule_to_python(TEST_RULES[5])
    {'dark olive': {'faded blue': 3, 'dotted black': 4}}
    >>> rule_to_python(TEST_RULES[6])
    {'vibrant plum': {'faded blue': 5, 'dotted black': 6}}
    >>> rule_to_python(TEST_RULES[7])
    {'faded blue': {}}
    >>> rule_to_python(TEST_RULES[8])
    {'dotted black': {}}
    """
    bag_color = bag_re.match(rule).group("color")
    contains = {
        m.group("color"): int(m.group("count")) for m in content_re.finditer(rule)
    }
    return {bag_color: contains}


def parse_rules(rules_list):
    rules = {}
    for rule in rules_list:
        rules.update(rule_to_python(rule))
    return rules


def is_bag_in_other_bag(bag_in, other_bag, rules):
    """Meh
    >>> is_bag_in_other_bag("shiny gold", "bright white", parse_rules(TEST_RULES))
    True
    >>> is_bag_in_other_bag("shiny gold", "muted yellow", parse_rules(TEST_RULES))
    True
    >>> is_bag_in_other_bag("shiny gold", "dark orange", parse_rules(TEST_RULES))
    True
    >>> is_bag_in_other_bag("shiny gold", "light red", parse_rules(TEST_RULES))
    True
    >>> is_bag_in_other_bag("shiny gold", "dark olive", parse_rules(TEST_RULES))
    False
    >>> is_bag_in_other_bag("shiny gold", "dotted black", parse_rules(TEST_RULES))
    False
    >>> is_bag_in_other_bag("shiny gold", "vibrant plum", parse_rules(TEST_RULES))
    False
    >>> is_bag_in_other_bag("shiny gold", "shiny gold", parse_rules(TEST_RULES))
    False
    """
    if bag_in in rules[other_bag]:
        return True

    for more in rules[other_bag].keys():
        if is_bag_in_other_bag(bag_in, more, rules):
            return True

    return False


def number_of_bags_can_contain(bag, rules):
    """Meh
    >>> number_of_bags_can_contain("shiny gold", parse_rules(TEST_RULES))
    4
    """
    n = 0
    for other_bag in rules.keys():
        if is_bag_in_other_bag(bag, other_bag, rules):
            # print(f"{bag} can fit in {other_bag}.")
            n += 1
    return n


def number_of_bags_in_bag(bag, rules):
    """Meh
    >>> number_of_bags_in_bag("shiny gold", parse_rules(TEST_RULES))
    32
    """
    num_bags = 0
    for other, count in rules[bag].items():
        num_bags += count + count * number_of_bags_in_bag(other, rules)
    return num_bags


if __name__ == "__main__":
    with open("input") as fd:
        rules = parse_rules(fd.read().strip().split("\n"))
    print(number_of_bags_can_contain("shiny gold", rules))
    print(number_of_bags_in_bag("shiny gold", rules))
