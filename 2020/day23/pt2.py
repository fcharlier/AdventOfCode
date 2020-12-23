#!/usr/bin/env python

EXAMPLE_INPUT = "389125467"
REAL_INPUT = "925176834"

"""
== DISCLAIMER

Using a sligtly improved algorithm base on pt1.py, I managed to get 100 moves done in
about 0.5s (initially) increasing to 3s around 300k rounds, that was not going to fit as
a solution. Too much data moving around behind the scenes.

Out of ideas this time I went to search for ideas on /r/adventofcode and realized that
a linked list was the way to go.

Rather than storing values in a list/array and rearranging them in memory, we instead
need to know for each value not its position (in a list) but which is the next value.
This way to pop or insert values after a certain value, we just need to change the
"next" one, which is only about writing a big value, but surely not moving large amounts
of data around.

So this is sadly not an algorighm which popped out of my head, but once I got the idea I
still wrote it by myself.

Runs in about 22s with Python 3
Runs in about 11s with PyPy 3

Machine: Intel(R) Core(TM) i5 CPU         750  @ 2.67GHz

% python3 -c "import sys; print(sys.version)"
Python 3.9.1 (default, Dec  8 2020, 00:00:00)
[GCC 10.2.1 20201125 (Red Hat 10.2.1-9)] on linux
% pypy3 --version
Python 3.6.9 (4d5bb11d5832, Aug 02 2020, 15:14:33)
[PyPy 7.3.1 with GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]

"""


def meh(text):
    """
    For each value "c", we store the next value,
    { val: val_next, otherval: otherval_next, … }

    >>> meh(EXAMPLE_INPUT)
    {3: 8, 8: 9, 9: 1, 1: 2, 2: 5, 5: 4, 4: 6, 6: 7, 7: 3}
    """
    return {int(c): int(text[(n + 1) % len(text)]) for n, c in enumerate(text)}


def mehMillion(text):
    """
    >>> m = mehMillion(EXAMPLE_INPUT)
    >>> len(m)
    1000000
    >>> max(m.keys())
    1000000
    >>> max(m.values())
    1000000
    >>> c = int(EXAMPLE_INPUT[0])
    >>> c == 3
    True
    >>> values = ""
    >>> for n in range(30):
    ...     values += str(c) + " "
    ...     c = m[c]
    ...
    >>> values
    '3 8 9 1 2 5 4 6 7 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 '
    """
    values = [int(c) for c in text]
    values.extend(list(range(max(values) + 1, 1000001)))
    return {v: values[(n + 1) % len(values)] for n, v in enumerate(values)}


def make_move(circle, cur_val):
    # Extract the 3 values after cur_val
    next_three = []
    for t in range(3):
        if not next_three:
            next_three.append(circle[cur_val])
        else:
            next_three.append(circle[next_three[-1]])
    # Now the value after cur_val is the value which was after the last one extracted
    circle[cur_val] = circle[next_three[-1]]

    # Search for the insertion value
    insert_after = (cur_val - 1) or len(circle)
    while insert_after in next_three:
        insert_after = (insert_after - 1) or len(circle)

    # And insert our three poped values after 'insert_after' & restore the link  (saved
    # in tmp) to the remaining of the circle
    tmp = circle[insert_after]
    for n in next_three:
        circle[insert_after] = n
        insert_after = n
    circle[insert_after] = tmp

    return circle[cur_val]


def print_circle(circle, start):
    for n in range(len(circle)):
        print(start, end=" ")
        start = circle[start]
    print()


def two_labels_after_1(circle):
    """
    >>> circ = mehMillion(EXAMPLE_INPUT)
    >>> cur_val = int(EXAMPLE_INPUT[0])
    >>> n = 0
    >>> for m in range(10000000):
    ...     cur_val = make_move(circ, cur_val)
    ...     n = m
    ...
    >>> n
    9999999
    >>> two_labels_after_1(circ)
    [934001, 159792]
    """
    pos = 1
    labels = []
    for n in range(2):
        labels.append(circle[pos])
        pos = circle[pos]
    return labels


def labels_after_1(circle):
    """
    >>> labels_after_1({8: 3, 3: 7, 7: 4, 4: 1, 1: 9, 9: 2, 2: 6, 6: 5, 5: 8})
    '92658374'
    >>> circ = meh(EXAMPLE_INPUT)
    >>> cur = int(EXAMPLE_INPUT[0])
    >>> for m in range(100):
    ...     cur = make_move(circ, cur)
    ...
    >>> labels_after_1(circ)
    '67384529'
    >>> circ = meh(REAL_INPUT)
    >>> cur = int(REAL_INPUT[0])
    >>> for m in range(100):
    ...     cur = make_move(circ, cur)
    ...
    >>> labels_after_1(circ)
    '69852437'
    """
    labels = ""
    nxt = circle[1]
    while nxt != 1:
        labels += str(nxt)
        nxt = circle[nxt]
    return labels


if __name__ == "__main__":
    circle = mehMillion(REAL_INPUT)
    MOVES = 10000000
    pos = int(REAL_INPUT[0])
    for n in range(MOVES):
        pos = make_move(circle, pos)
    labels = two_labels_after_1(circle)
    answer = labels[0] * labels[1]
    print(
        f"After {MOVES} moves, the labels on the cups after cup 1 are: {labels}. "
        f"Multiplying them together gives: {answer}."
    )
