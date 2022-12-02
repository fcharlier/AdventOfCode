#!/usr/bin/python3

RPS = {
    "A": "ROCK",
    "B": "PAPER",
    "C": "SCISSORS",
    "X": "LOSE",
    "Y": "DRAW",
    "Z": "WIN",
}

OUTCOMES = {
    "LOSE": 0,
    "DRAW": 3,
    "WIN": 6,
    "ROCK": {
        "VALUE": 1,
        "LOSE": "SCISSORS",
        "DRAW": "ROCK",
        "WIN": "PAPER",
    },
    "PAPER": {
        "VALUE": 2,
        "LOSE": "ROCK",
        "DRAW": "PAPER",
        "WIN": "SCISSORS",
    },
    "SCISSORS": {
        "VALUE": 3,
        "LOSE": "PAPER",
        "DRAW": "SCISSORS",
        "WIN": "ROCK",
    },
}


def score(p1, p2):
    """
    >>> score("A", "Y")
    4
    >>> score("B", "X")
    1
    >>> score("C", "Z")
    7
    """
    p1 = RPS[p1]
    p2 = RPS[p2]

    return OUTCOMES[p2] + OUTCOMES[OUTCOMES[p1][p2]]["VALUE"]

if __name__ == '__main__':
    with open("input_real") as fd:
        result = sum([score(*line.strip().split(" ")) for line in fd])
        print(result)
