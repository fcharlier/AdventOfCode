#!/usr/bin/env python


import itertools

EXAMPLE_INPUT = """35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576
"""


def input2list(text):
    return [int(line.strip()) for line in text.strip().split()]


def sums(numbers, choices):
    return (a + b for a, b in itertools.combinations(numbers, choices))


def isvalid(number, numbers, choices=2):
    """Meh
    >>> isvalid(40, (35, 20, 15, 25, 47))
    True
    >>> isvalid(62, (20, 15, 25, 47, 40))
    True
    >>> isvalid(127, (182, 150, 117, 102, 95))
    False
    """
    return number in sums(numbers, choices)


def firstinvalid(numbers, length, choices):
    """Meh
    >>> firstinvalid(input2list(EXAMPLE_INPUT), 5, 2)
    127
    """
    for i in range(length, len(numbers)):
        if not isvalid(numbers[i], numbers[i - length : i]):
            return numbers[i]
    return None


def sumtoinvalid(numbers, invalid):
    """Meh
    >>> sumtoinvalid(input2list(EXAMPLE_INPUT), 127)
    62
    """
    invalid_index = numbers.index(invalid)
    for n in range(invalid_index):
        for m in range(n + 1, invalid_index - 1):
            nb_slice = numbers[n:m]
            if sum(nb_slice) == invalid:
                return min(nb_slice) + max(nb_slice)


if __name__ == "__main__":
    with open("input") as fd:
        numbers = input2list(fd.read())
    invalid = firstinvalid(numbers, 25, 2)
    print("part 1:", invalid)
    print("part 2:", sumtoinvalid(numbers, invalid))
