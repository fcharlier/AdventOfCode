#!/usr/bin/python3


def read_input(filename):
    with open(filename) as fd:
        return [line.strip().split(" ") for line in fd.readlines()]


def draw(cycle, X, screen):
    row = (cycle - 1) // 40
    col = (cycle - 1) % 40

    if X - 1 <= col <= X + 1:
        screen[row][col] = "#"


def do_cycles(instructions):
    """Meh
    >>> instructions = read_input("input_example")
    >>> r = do_cycles(instructions)
    >>> r.split("\\n")[0]
    '##..##..##..##..##..##..##..##..##..##..'
    >>> r.split("\\n")[1]
    '###...###...###...###...###...###...###.'
    >>> r.split("\\n")[2]
    '####....####....####....####....####....'
    >>> r.split("\\n")[3]
    '#####.....#####.....#####.....#####.....'
    >>> r.split("\\n")[4]
    '######......######......######......####'
    >>> r.split("\\n")[5]
    '#######.......#######.......#######.....'
    """
    cycle = 1
    X = 1
    screen = []
    for row in range(6):
        screen.append([])
        for col in range(40):
            screen[row].append(".")

    for instruction in instructions:
        if instruction[0] == "noop":
            draw(cycle, X, screen)
            cycle += 1
            if cycle >= 240:
                break
        elif instruction[0] == "addx":
            value = int(instruction[1])
            draw(cycle, X, screen)
            cycle += 1
            if cycle >= 240:
                break
            draw(cycle, X, screen)
            X += value
            cycle += 1
            if cycle >= 240:
                break
    return("\n".join(["".join(line) for line in screen]))


if __name__ == "__main__":
    print(do_cycles(read_input("input_real")).replace(".", " "))
