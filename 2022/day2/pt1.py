#!/usr/bin/python3

RPS = {
    "A": "ROCK",
    "B": "PAPER",
    "C": "SCISSORS",
    "X": "ROCK",
    "Y": "PAPER",
    "Z": "SCISSORS",
}

OUTCOMES = {
    "ROCK": {
        "VALUE": 1,
        "ROCK": 3,
        "PAPER": 6,
        "SCISSORS": 0,
    },
    "PAPER": {
        "VALUE": 2,
        "ROCK": 0,
        "PAPER": 3,
        "SCISSORS": 6,
    },
    "SCISSORS": {
        "VALUE": 3,
        "ROCK": 6,
        "PAPER": 0,
        "SCISSORS": 3,
    },
}


def score(p1, p2):
    """
    >>> score("A", "Y")
    8
    >>> score("B", "X")
    1
    >>> score("C", "Z")
    6
    """
    p1 = RPS[p1]
    p2 = RPS[p2]

    return OUTCOMES[p1][p2] + OUTCOMES[p2]["VALUE"]

if __name__ == '__main__':
    with open("input_real") as fd:
        result = sum([score(*line.strip().split(" ")) for line in fd])
        print(result)
