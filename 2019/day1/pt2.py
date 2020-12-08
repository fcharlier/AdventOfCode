#!/usr/bin/python3


def fuel(mass):
    """Blah

    >>> fuel(14)
    2
    >>> fuel(1969)
    966
    """
    _fuel = mass // 3 - 2
    total = 0
    while _fuel > 0:
        total += _fuel
        _fuel = _fuel // 3 - 2
    return total


if __name__ == "__main__":
    with open("data") as data:
        lines = data.readlines()
    masses = map(int, lines)
    fuel = map(fuel, masses)
    print(sum(fuel))
