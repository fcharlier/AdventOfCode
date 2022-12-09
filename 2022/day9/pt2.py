#!/usr/bin/python3


def parse_input(filename):
    """Reads filename into a useful data structure
    >>> moves = parse_input("input_example")
    >>> len(moves)
    8
    >>> moves[0]
    ('R', 4)
    >>> moves[7]
    ('R', 2)
    """
    with open(filename) as fd:
        motions = [line.strip().split(" ") for line in fd]
    return [(direction, int(count)) for (direction, count) in motions]


def do_moves(moves, rope_len):
    """Applies the moves and returns the number of positions visited by the tail
    >>> moves = parse_input("input_example")
    >>> do_moves(moves, 2)
    13
    >>> do_moves(moves, 10)
    1
    >>> moves = parse_input("input_example2")
    >>> do_moves(moves, 10)
    36
    """
    DIRS = {
        "R": (1, 0),
        "L": (-1, 0),
        "U": (0, 1),
        "D": (0, -1),
    }

    tail_records = set()
    rope = [[0, 0] for _ in range(rope_len)]

    for (direction, count) in moves:
        for n in range(count):
            rope[0][0] += DIRS[direction][0]
            rope[0][1] += DIRS[direction][1]
            for knot in range(1, rope_len):
                diff0 = rope[knot - 1][0] - rope[knot][0]
                diff1 = rope[knot - 1][1] - rope[knot][1]
                if abs(diff0) > 1 or abs(diff1) > 1:
                    rope[knot][0] += diff0 // abs(diff0) if diff0 else 0
                    rope[knot][1] += diff1 // abs(diff1) if diff1 else 0
            tail_records.add(",".join(map(str, rope[rope_len - 1])))
    return len(tail_records)


if __name__ == "__main__":
    moves = parse_input("input_real")
    print(do_moves(moves, 10))
