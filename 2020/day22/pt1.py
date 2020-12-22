#!/usr/bin/env python

EXAMPLE = """Player 1:
9
2
6
3
1

Player 2:
5
8
4
7
10
"""


def get_decks(text):
    """
    >>> get_decks(EXAMPLE)
    [[9, 2, 6, 3, 1], [5, 8, 4, 7, 10]]
    """
    decks = [[], []]
    p = 0
    for line in text.strip().split("\n"):
        if line.startswith("Player"):
            continue
        if line == "":
            p += 1
            continue
        decks[p].append(int(line))

    return decks


def play_round(decks):
    cardp1, decks[0] = decks[0][0], decks[0][1:]
    cardp2, decks[1] = decks[1][0], decks[1][1:]
    if cardp1 > cardp2:
        decks[0].extend([cardp1, cardp2])
    else:
        decks[1].extend([cardp2, cardp1])


def play_game(decks):
    """
    >>> play_game(get_decks(EXAMPLE))
    306
    """
    while all((len(deck) for deck in decks)):
        play_round(decks)

    score = sum(
        (k + 1) * v for k, v in enumerate(reversed([n for deck in decks for n in deck]))
    )
    return score


if __name__ == "__main__":
    with open("input") as fd:
        decks = get_decks(fd.read())

    score = play_game(decks)
    print(f"Final score: {score}")
