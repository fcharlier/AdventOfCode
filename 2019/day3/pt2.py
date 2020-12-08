#!/usr/bin/python3

import numpy as np


def boundaries(w_one, w_two):
    """Returns the boundaries of a wire

    >>> boundaries(["R8", "U5", "L5", "D3"])
    {'top': 5, 'bottom': 0, 'left': 0, 'right': 8}
    """
    top = bottom = left = right = 0

    for wire in (w_one, w_two):
        vert = 0
        horz = 0
        for move in wire:
            if move[0] == "U":
                vert += int(move[1:])
                top = max(top, vert)
            elif move[0] == "D":
                vert -= int(move[1:])
                bottom = min(bottom, vert)
            elif move[0] == "L":
                horz -= int(move[1:])
                left = min(left, horz)
            elif move[0] == "R":
                horz += int(move[1:])
                right = max(right, horz)

    return {
        "top": top,
        "bottom": bottom,
        "left": left,
        "right": right,
        "width": right - left + 1,
        "height": top - bottom + 1,
        "0x": -left,
        "0y": -bottom,
    }


def parse_input(input_str):
    """Parse the wires path
    """
    w_one, w_two = input_str.strip().split("\n")
    w_one = w_one.split(",")
    w_two = w_two.split(",")

    return w_one, w_two


def min_steps(steps, cell):
    if cell[1] and cell[2]:
        tot = cell[1] + cell[2]
        if steps is None:
            return tot
        return min(steps, tot)
    return steps


def trace_wire(wire, wiremap, bbox, id):
    x, y = bbox["0x"], bbox["0y"]
    step = 1
    steps = None

    for move in wire:
        count = int(move[1:])
        if move[0] == "U":
            while count > 0:
                y += 1
                if wiremap[y][x][id] == 0:
                    wiremap[y][x][id] = step
                count -= 1
                step += 1
                steps = min_steps(steps, wiremap[y][x])
        elif move[0] == "D":
            while count > 0:
                y -= 1
                if wiremap[y][x][id] == 0:
                    wiremap[y][x][id] = step
                count -= 1
                step += 1
                steps = min_steps(steps, wiremap[y][x])
        elif move[0] == "L":
            while count > 0:
                x -= 1
                if wiremap[y][x][id] == 0:
                    wiremap[y][x][id] = step
                count -= 1
                step += 1
                steps = min_steps(steps, wiremap[y][x])
        elif move[0] == "R":
            while count > 0:
                x += 1
                if wiremap[y][x][id] == 0:
                    wiremap[y][x][id] = step
                count -= 1
                step += 1
                steps = min_steps(steps, wiremap[y][x])

    if steps:
        print(steps)


def mkmap(w_one, w_two, bbox):
    wiremap = np.zeros((bbox["height"] + 1, bbox["width"] + 1, 3), np.int32)
    trace_wire(w_one, wiremap, bbox, 1)
    trace_wire(w_two, wiremap, bbox, 2)
    return wiremap


if __name__ == "__main__":
    with open("data") as data:
        w_one, w_two = parse_input(data.read())

    bbox = boundaries(w_one, w_two)
    mkmap(w_one, w_two, bbox)
