#!/usr/bin/env python


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
    with open(filename) as fd:
        for line in fd:
            digits, values = line.split("|")
            data.append([digits.strip().split(), values.strip().split()])
    return data


def count_one_four_seven_eight(data):
    """
    >>> data = read_input('example')
    >>> count_one_four_seven_eight(data)
    26
    """
    onefourseveneights = 0
    for digits, values in data:
        vlengths = [len(value) for value in values]
        onefourseveneights += sum(1 if vlen in (2, 3, 4, 7) else 0 for vlen in vlengths)
    return onefourseveneights


if __name__ == "__main__":
    data = read_input('input')
    print(count_one_four_seven_eight(data))
