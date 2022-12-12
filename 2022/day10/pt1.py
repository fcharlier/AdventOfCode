#!/usr/bin/python3


def read_input(filename):
    with open(filename) as fd:
        return [line.strip().split(" ") for line in fd.readlines()]


def eval_signal_strength(cycle, X, strengths):
    if cycle in (20, 60, 100, 140, 180, 220):
        strengths.append(cycle * X)

def do_cycles(instructions):
    """ Meh
    >>> instructions = read_input("input_example")
    >>> r = do_cycles(instructions)
    >>> r
    [420, 1140, 1800, 2940, 2880, 3960]
    >>> sum(r)
    13140
    """
    cycle = 1
    X = 1
    signal_strengths = []

    for instruction in instructions:
        if instruction[0] == "noop":
            cycle += 1
            eval_signal_strength(cycle, X, signal_strengths)
        elif instruction[0] == "addx":
            value = int(instruction[1])
            cycle += 1
            eval_signal_strength(cycle, X, signal_strengths)
            cycle += 1
            X += value
            eval_signal_strength(cycle, X, signal_strengths)
    return signal_strengths


if __name__ == "__main__":
    print(sum(do_cycles(read_input("input_real"))))
