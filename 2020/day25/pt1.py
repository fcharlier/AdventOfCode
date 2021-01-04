#!/usr/bin/env python

EXAMPLE_K1 = 5764801
EXAMPLE_K2 = 17807724

INPUT_K1 = 11239946
INPUT_K2 = 10464955


def cycle(value, subjectnum):
    """
    >>> value = 1
    >>> for _ in range(11):
    ...     value = cycle(value, 5764801)
    >>> value
    14897079
    >>> value = 1
    >>> for _ in range(8):
    ...     value = cycle(value, 17807724)
    >>> value
    14897079
    """
    value *= subjectnum
    value %= 20201227
    return value


def guess_cyclecount(key):
    """Meh
    >>> guess_cyclecount(EXAMPLE_K1)
    8
    >>> guess_cyclecount(EXAMPLE_K2)
    11
    """
    n = 0
    value = 1
    while value != key:
        n += 1
        value = cycle(value, 7)
    return n


if __name__ == "__main__":
    K1_ccount = guess_cyclecount(INPUT_K1)
    K2_ccount = guess_cyclecount(INPUT_K2)

    key1 = 1
    for _ in range(K1_ccount):
        key1 = cycle(key1, INPUT_K2)

    key2 = 1
    for _ in range(K2_ccount):
        key2 = cycle(key2, INPUT_K1)

    print(f"Key1: {key1}, Key2: {key2}")
