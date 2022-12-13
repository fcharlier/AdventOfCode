#!/usr/bin/python3

from ast import literal_eval
from itertools import zip_longest


def in_order(left, right, shift=0):
    """
    >>> in_order([1,1,3,1,1], [1,1,5,1,1])
    True
    >>> in_order([[1],[2,3,4]], [[1],4])
    True
    >>> in_order([9], [[8,7,6]])
    False
    >>> in_order([[4,4],4,4], [[4,4],4,4,4])
    True
    >>> in_order([7,7,7,7], [7,7,7])
    False
    >>> in_order([], [3])
    True
    >>> in_order([[[]]], [[]])
    False
    >>> in_order([1,[2,[3,[4,[5,6,7]]]],8,9], [1,[2,[3,[4,[5,6,0]]]],8,9])
    False
    >>> in_order([[],7], [[3]])
    True
    """
    # print("  " * shift, f"- Compare {left} with {right}")
    shift += 1
    for lft, rgt in zip_longest(left, right):
        # print("  " * shift, f"- Compare {lft} with {rgt}")
        if isinstance(lft, int) and isinstance(rgt, int):
            if lft > rgt:
                # print(
                #     "  " * (shift + 1),
                #     "- Right side is smaller, so inputs are NOT in the right order",
                # )
                return False
            if lft < rgt:
                # print(
                #     "  " * (shift + 1),
                #     "- Left side is smaller, so inputs are in the RIGHT order",
                # )
                return True
        elif isinstance(lft, list) and isinstance(rgt, list):
            if (result := in_order(lft, rgt, shift + 1)) is not None:
                return result
        elif isinstance(lft, list) and isinstance(rgt, int):
            # print(
            #     "  " * shift,
            #     f"- Mixed types; convert right to [{rgt}] and retry comparison",
            # )
            if (
                result := in_order(
                    lft,
                    [
                        rgt,
                    ],
                    shift + 1,
                )
            ) is not None:
                return result
        elif isinstance(lft, int) and isinstance(rgt, list):
            # print(
            #     "  " * shift,
            #     f"- Mixed types; convert left to [{lft}] and retry comparison",
            # )
            if (
                result := in_order(
                    [
                        lft,
                    ],
                    rgt,
                    shift + 1,
                )
            ) is not None:
                return result
        elif lft is None and rgt is not None:
            # print(
            #     "  " * (shift + 1),
            #     "- Left side ran out of items, so inputs are in the RIGHT order.",
            # )
            return True
        elif lft is not None and rgt is None:
            # print(
            #     "  " * (shift + 1),
            #     "- Right side ran out of items, so inputs are NOT in the right order.",
            # )
            return False
    return None


def read_input(filename):
    """
    >>> pairs = read_input("input_example")
    >>> len(pairs)
    8
    >>> pairs[0][0]
    [1, 1, 3, 1, 1]
    >>> pairs[6][0]
    [[[]]]
    """
    pairs = []
    elts = []
    with open(filename) as fd:
        for line in fd:
            line = line.strip()
            if not len(line):
                continue
            elts.append(literal_eval(line))
            if len(elts) == 2:
                pairs.append(elts)
                elts = []
    return pairs


def sumcorrect(pairs):
    """
    >>> pairs = read_input("input_example")
    >>> sumcorrect(pairs)
    13
    """
    corrects = 0
    for n, p in enumerate(pairs):
        # print(f"== Pair {n+1} ==")
        if in_order(*p):
            corrects += n + 1

    return corrects
    # return sum([n + 1 for n, p in enumerate(pairs) if in_order(*p)])


if __name__ == "__main__":
    pairs = read_input("input_real")
    print(sumcorrect(pairs))
