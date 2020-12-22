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

GAME = 0


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


def play_round(decks, game, r):
    # print(f"-- Round {r} (Game {game})")
    # print("Player 1's deck:", ", ".join(str(v) for v in decks[0]))
    # print("Player 2's deck:", ", ".join(str(v) for v in decks[1]))
    cardp1, decks[0] = decks[0][0], decks[0][1:]
    cardp2, decks[1] = decks[1][0], decks[1][1:]
    # print(f"Player 1 plays: {cardp1}")
    # print(f"Player 2 plays: {cardp2}")

    if cardp1 <= len(decks[0]) and cardp2 <= len(decks[1]):
        # print("Playing a sub-game to determine the winner ...\n")
        _, newd = play_game([decks[0][:cardp1], decks[1][:cardp2]])
        # print(f"...anyway, back to game {game}")
        if len(newd[0]) > 0:
            # print(f"Player 1 wins round {r} of game {game}!\n")
            decks[0].extend([cardp1, cardp2])
        else:
            # print(f"Player 2 wins round {r} of game {game}!\n")
            decks[1].extend([cardp2, cardp1])
    else:
        if cardp1 > cardp2:
            # print(f"Player 1 wins round {r} of game {game}!\n")
            decks[0].extend([cardp1, cardp2])
        else:
            # print(f"Player 2 wins round {r} of game {game}!\n")
            decks[1].extend([cardp2, cardp1])


def play_game(decks):
    """
    >>> play_game(get_decks(EXAMPLE))
    (291, [[], [7, 5, 6, 2, 4, 1, 10, 8, 9, 3]])
    """
    global GAME
    GAME += 1
    game = GAME
    # print(f"=== Game {game} ===\n")

    previous_hands = [[], []]
    n = 0
    while all((len(deck) for deck in decks)):
        n += 1
        hands = [",".join(str(d)) for d in decks]
        if hands[0] in previous_hands[0] or hands[1] in previous_hands[1]:
            # print(f"Recursion in game {game} round {n} for hands {hands}")
            return 666, [[1], []]
        else:
            previous_hands[0].append(hands[0])
            previous_hands[1].append(hands[1])

        play_round(decks, game=game, r=n)

    score = sum(
        (k + 1) * v for k, v in enumerate(reversed([n for deck in decks for n in deck]))
    )
    # if len(decks[0]) > 0:
    #     print(f"The winner of game {game} is player 1\n")
    # elif len(decks[1]) > 0:
    #     print(f"The winner of game {game} is player 2\n")
    return score, decks


if __name__ == "__main__":
    with open("input") as fd:
        decks = get_decks(fd.read())
    score, decks = play_game(decks)
    print(f"Final score: {score}")
