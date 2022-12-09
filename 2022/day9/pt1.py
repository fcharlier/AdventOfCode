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


def do_moves(moves):
    """Applies the moves and returns the number of positions visited by the tail
    >>> moves = parse_input("input_example")
    >>> do_moves(moves)
    13
    """
    DIRS = {
        "R": (1, 0),
        "L": (-1, 0),
        "U": (0, 1),
        "D": (0, -1),
    }

    tail_records = set()
    head = [0, 0]
    tail = [0, 0]

    for (direction, count) in moves:
        # print(f"== {direction} {count} ==")
        for n in range(count):
            head[0] += DIRS[direction][0]
            head[1] += DIRS[direction][1]
            # print(f"H: {head}")
            if abs(head[0] - tail[0]) > 1:
                tail[0] += DIRS[direction][0]
                tail[1] = head[1]
            elif abs(head[1] - tail[1]) > 1:
                tail[1] += DIRS[direction][1]
                tail[0] = head[0]
            # print(f"T: {tail}")

            tail_records.add(",".join(map(str, tail)))

    return len(tail_records)


if __name__ == "__main__":
    moves = parse_input("input_real")
    print(do_moves(moves))
