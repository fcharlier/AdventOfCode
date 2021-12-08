#!/usr/bin/env python

""" Meh
"""

SAMPLE = [
    [
        "acedgfb",
        "cdfbe",
        "gcdfa",
        "fbcad",
        "dab",
        "cefabd",
        "cdfgeb",
        "eafb",
        "cagedb",
        "ab",
    ],
    ["cdfeb", "fcadb", "cdfeb", "cdbaf"],
]


def read_input(filename):
    """
    >>> data = read_input('example')
    >>> len(data)
    10
    >>> len(data[0])
    2
    >>> len(data[1])
    2
    >>> len(data[0][0])
    10
    >>> len(data[0][1])
    4
    """
    data = []
    with open(filename) as in_fd:
        for line in in_fd:
            digits, values = line.split("|")
            data.append([digits.strip().split(), values.strip().split()])
    return data


def zero(data, known):
    """
    >>> known = easy_ones(SAMPLE)
    >>> known[9] = nine(SAMPLE, known)
    >>> known[6] = six(SAMPLE, known)
    >>> zero(SAMPLE, known)
    'cagedb'
    """
    len6 = list(filter(lambda d: len(d) == 6, data[0]))
    len6.remove(known[9])
    len6.remove(known[6])
    return len6[0]


def one(data):
    """
    >>> one(SAMPLE)
    'ab'
    """
    return list(filter(lambda d: len(d) == 2, data[0]))[0]


def two(data, known):
    """
    >>> known = easy_ones(SAMPLE)
    >>> two(SAMPLE, known)
    'gcdfa'
    """
    len5 = list(filter(lambda d: len(d) == 5, data[0]))
    for digit in len5:
        if (
            len(set(digit) - set(known[7])) == 3
            and len(set(digit) - set(known[4])) == 3
        ):
            return digit
    return None


def three(data, known):
    """
    >>> known = easy_ones(SAMPLE)
    >>> three(SAMPLE, known)
    'fbcad'
    """
    len5 = list(filter(lambda d: len(d) == 5, data[0]))
    for digit in len5:
        if (
            len(set(digit) - set(known[7])) == 2
            and len(set(digit) - set(known[4])) == 2
        ):
            return digit
    return None


def four(data):
    """
    >>> four(SAMPLE)
    'eafb'
    """
    return list(filter(lambda d: len(d) == 4, data[0]))[0]


def five(data, known):
    """
    >>> known = easy_ones(SAMPLE)
    >>> five(SAMPLE, known)
    'cdfbe'
    """
    len5 = list(filter(lambda d: len(d) == 5, data[0]))
    for digit in len5:
        if (
            len(set(digit) - set(known[7])) == 3
            and len(set(digit) - set(known[4])) == 2
        ):
            return digit
    return None


def six(data, known):
    """
    >>> known = easy_ones(SAMPLE)
    >>> known[9] = nine(SAMPLE, known)
    >>> six(SAMPLE, known)
    'cdfgeb'
    """
    len6 = list(filter(lambda d: len(d) == 6, data[0]))
    len6.remove(known[9])
    for digit in len6:
        if len(set(digit) - set(known[7])) == 4:
            return digit
    return None


def seven(data):
    """
    >>> seven(SAMPLE)
    'dab'
    """
    return list(filter(lambda d: len(d) == 3, data[0]))[0]


def eight(data):
    """
    >>> eight(SAMPLE)
    'acedgfb'
    """
    return list(filter(lambda d: len(d) == 7, data[0]))[0]


def nine(data, known):
    """
    >>> nine(SAMPLE, easy_ones(SAMPLE))
    'cefabd'
    """
    len6 = list(filter(lambda d: len(d) == 6, data[0]))
    for digit in len6:
        if len(set(digit).difference(set(known[7] + known[4]))) == 1:
            return digit
    return None


def easy_ones(data):
    """ Meh
    """
    known = [
        "",
    ] * 10
    known[1] = one(data)
    known[4] = four(data)
    known[7] = seven(data)
    known[8] = eight(data)
    return known


def guess_digits(data):
    """
    >>> len(guess_digits(SAMPLE))
    10
    """
    known = easy_ones(data)
    known[9] = nine(data, known)
    known[6] = six(data, known)
    known[0] = zero(data, known)
    known[3] = three(data, known)
    known[5] = five(data, known)
    known[2] = two(data, known)
    return {"".join(sorted(v)): k for k, v in enumerate(known)}


def entry_value(data):
    """
    >>> entry_value(SAMPLE)
    5353
    """
    digits = guess_digits(data)
    entry = 0
    for d in data[1]:
        entry = entry * 10 + digits["".join(sorted(d))]
    return entry


def whole_puzzle(entries):
    """
    >>> entries = read_input('example')
    >>> whole_puzzle(entries)
    ([8394, 9781, 1197, 9361, 4873, 8418, 4548, 1625, 8717, 4315], 61229)
    """
    outputs = []
    for entry in entries:
        outputs.append(entry_value(entry))
    return outputs, sum(outputs)


if __name__ == "__main__":
    entries = read_input("input")
    print(whole_puzzle(entries)[1])
