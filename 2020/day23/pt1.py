#!/usr/bin/env python

EXAMPLE_INPUT = "389125467"


def meh(text):
    """
    >>> meh(EXAMPLE_INPUT)
    [3, 8, 9, 1, 2, 5, 4, 6, 7]
    """
    return [int(c) for c in text]


def destination_index(circle):
    """
    >>> destination_index([3, 2, 5, 4, 6, 7])
    (2, 1)
    >>> destination_index([2, 5, 4, 6, 7, 3])
    (7, 4)
    >>> destination_index([5, 8, 9, 1, 3, 2])
    (3, 4)
    """
    val_next = circle[0] - 1
    while val_next not in circle:
        val_next -= 1
        if val_next < 0:
            val_next = max(circle)
    return val_next, circle.index(val_next)


def pick_three(circle):
    """
    >>> pick_three([3, 8, 9, 1, 2, 5, 4, 6, 7])
    ([3, 2, 5, 4, 6, 7], [8, 9, 1])
    >>> pick_three([1, 3, 6, 7, 9, 2, 5, 8, 4])
    ([1, 9, 2, 5, 8, 4], [3, 6, 7])
    """
    circle, three = circle[:1] + circle[4:], circle[1:4]
    return circle, three


def insert_after(circle, three, pos):
    """
    >>> insert_after([3, 2, 5, 4, 6, 7], [8, 9, 1], 1)
    [3, 2, 8, 9, 1, 5, 4, 6, 7]
    >>> insert_after([1, 9, 2, 5, 8, 4], [3, 6, 7], 1)
    [1, 9, 3, 6, 7, 2, 5, 8, 4]
    """
    return circle[: pos + 1] + three + circle[pos + 1 :]


def make_move(circle):
    """
    >>> n = make_move(meh(EXAMPLE_INPUT))
    >>> n
    [2, 8, 9, 1, 5, 4, 6, 7, 3]
    >>> n = make_move(n)
    >>> n
    [5, 4, 6, 7, 8, 9, 1, 3, 2]
    >>> circ = meh(EXAMPLE_INPUT)
    >>> for m in range(10):
    ...     circ = make_move(circ)
    ...
    >>> circ
    [8, 3, 7, 4, 1, 9, 2, 6, 5]
    """
    circle, three = pick_three(circle)
    val, d = destination_index(circle)
    circle = insert_after(circle, three, d)
    circle.append(circle.pop(0))
    return circle


def labels_after_1(circle):
    """
    >>> labels_after_1([8, 3, 7, 4, 1, 9, 2, 6, 5])
    '92658374'
    >>> circ = meh(EXAMPLE_INPUT)
    >>> for m in range(100):
    ...     circ = make_move(circ)
    ...
    >>> labels_after_1(circ)
    '67384529'
    """
    n = circle.index(1)
    res = circle[n+1:] + circle[:n]
    return "".join(str(r) for r in res)


if __name__ == "__main__":
    circle = meh("925176834")
    for n in range(100):
        circle = make_move(circle)
    answer = labels_after_1(circle)
    print(f"After 100 moves, the labels on the cups after cup 1 are: {answer}.")
