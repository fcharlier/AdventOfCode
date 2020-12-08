#!/usr/bin/env python

from itertools import chain

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
        result.append(set(line.strip()) for line in group.split("\n"))
    return result


def unique_answers(group):
    """Meh
    >>> sorted(unique_answers([{"a", "b", "c"}]))
    ['a', 'b', 'c']
    >>> sorted(unique_answers([{"a"}, {"b"}, {"c"}]))
    ['a', 'b', 'c']
    >>> sorted(unique_answers([{"a", "b"}, {"a", "c"}]))
    ['a', 'b', 'c']
    >>> unique_answers([{"c"}, {"c"}, {"c"}])
    {'c'}
    """
    return set(chain(*group))


def poll_answers_sum(poll):
    """Meh
    >>> poll_answers_sum(TEST_POLL)
    11
    """
    groups = split_groups(poll)
    answers_count = (len(unique_answers(group)) for group in groups)
    poll_answers = sum(answers_count)
    return poll_answers


if __name__ == "__main__":
    with open("input") as fd:
        poll = fd.read()

    print(poll_answers_sum(poll))
