#!/usr/bin/env python


def throw_dice(start, count):
    """
    >>> throw_dice(1, 3)[0]
    6
    >>> throw_dice(7, 3)[0]
    24
    >>> throw_dice(98, 3)[0]
    297
    >>> throw_dice(99, 3)[0]
    200
    >>> throw_dice(100, 3)[0]
    103
    """
    numbers = [(n - 1) % 100 + 1 for n in range(start, start + 3)]
    return sum(numbers), numbers


def play_dice(p1_pos, p2_pos):
    """
    >>> play_dice(4, 8)
    739785
    """
    pos = [p1_pos - 1, p2_pos - 1]
    scores = [0, 0]
    turn = 0
    while all(scores[n] < 1000 for n in range(2)):
        throw, dices = throw_dice(turn * 3 + 1, 3)
        player = turn % 2
        pos[player] = (pos[player] + throw) % 10
        scores[player] += pos[player] + 1
        # print(
        #     f"Player {player + 1} rolls {dices} and moves to space "
        #     f"{pos[player] + 1} for a total score of {scores[player]}"
        # )
        turn += 1
    return min(scores) * turn * 3


if __name__ == "__main__":
    print(play_dice(6, 9))
