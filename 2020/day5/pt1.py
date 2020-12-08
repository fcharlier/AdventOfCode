#!/usr/bin/env python

"""
Have you noticed how the boarding pass code for the place is a binary representation of
the place number ?
This is however witten black on white in the instructions ^_^
Took me a while to realize it XD
"""


def guessrow(code):
    """ Not used in fine, used to validate given examples before I realized that the
    whole boardingpass was a binary number when I re-read the instructions carefully.
    >>> guessrow("FBFBBFF")
    44
    >>> guessrow("BFFFBBF")
    70
    >>> guessrow("FFFBBBF")
    14
    >>> guessrow("BBFFBBF")
    102
    """

    code = code.translate(code.maketrans("BF", "10"))
    return int(code, 2)


def guesscol(code):
    """ Not used in fine, used to validate given examples before I realized that the
    whole boardingpass was a binary number when I re-read the instructions carefully.
    >>> guesscol("RLR")
    5
    >>> guesscol("RRR")
    7
    >>> guesscol("RLL")
    4
    """

    code = code.translate(code.maketrans("RL", "10"))
    return int(code, 2)


def seatid(code):
    """ The code on the boarding pass is a binary representation of the place number …
    Just convert B & R to 1 and F & R to 0.
    >>> seatid("BFFFBBFRRR")
    567
    >>> seatid("FFFBBBFRRR")
    119
    >>> seatid("BBFFBBFRLL")
    820
    """
    code = code.translate(code.maketrans("BFRL", "1010"))
    return int(code, 2)


def guessseat(seatids):
    """ Our seat is the seat which id is not in the least but which previous & next one
    is in.
    """
    for seat in seatids:
        if seat + 1 not in seatids and seat + 2 in seatids:
            return seat + 1


if __name__ == "__main__":
    with open("input") as fd:
        boardingpasses = (boardingpass.strip() for boardingpass in fd.readlines())

    seatids = list((seatid(bp) for bp in boardingpasses))
    print("Maximum seat id:",  max(seatids))
    print("Your seat id:", guessseat(seatids))
