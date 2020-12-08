#!/usr/bin/env python

from functools import reduce

TEST_POLL = """abc

a
b
c

ab
ac

a
a
a
a

b
"""


def split_groups(poll):
    result = []
    for group in poll.split("\n\n"):
        result.append(set(line.strip()) for line in group.strip().split("\n"))
    return result


def answers_all_yes(group):
    """Meh
    >>> sorted(answers_all_yes([{"a", "b", "c"}]))
    ['a', 'b', 'c']
    >>> sorted(answers_all_yes([{"a"}, {"b"}, {"c"}]))
    []
    >>> sorted(answers_all_yes([{"a", "b"}, {"a", "c"}]))
    ['a']
    >>> answers_all_yes([{"c"}, {"c"}, {"c"}])
    {'c'}
    """

    return reduce(lambda x, y: x & y, group)


def poll_answers_sum(poll):
    """Meh
    >>> poll_answers_sum(TEST_POLL)
    6
    """
    groups = split_groups(poll)
    answers_count = (len(answers_all_yes(group)) for group in groups)
    poll_answers = sum(answers_count)
    return poll_answers


if __name__ == "__main__":
    with open("input") as fd:
        poll = fd.read()

    print(poll_answers_sum(poll))
