#!/usr/bin/python3

import numpy as np
from scipy.misc import imshow


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


def trace_wire(wire, wiremap, bbox, inc):
    x, y = bbox["0x"], bbox["0y"]

    for move in wire:
        count = int(move[1:])
        if move[0] == "U":
            while count > 0:
                y += 1
                wiremap[y][x] += inc
                count -= 1
        elif move[0] == "D":
            while count > 0:
                y -= 1
                wiremap[y][x] += inc
                count -= 1
        elif move[0] == "L":
            while count > 0:
                x -= 1
                wiremap[y][x] += inc
                count -= 1
        elif move[0] == "R":
            while count > 0:
                x += 1
                wiremap[y][x] += inc
                count -= 1


def mkmap(w_one, w_two, bbox):
    wiremap = np.zeros((bbox["height"] + 1, bbox["width"] + 1), np.int8)
    wiremap[bbox["0y"]][bbox["0x"]] = -10
    trace_wire(w_one, wiremap, bbox, 15)
    trace_wire(w_two, wiremap, bbox, 30)
    return wiremap


if __name__ == "__main__":
    with open("data") as data:
        w_one, w_two = parse_input(data.read())
    # w_one, w_two = parse_input("L8,U5,R5,D3\nU7,L6,D4,R4")
    # w_one, w_two = parse_input("R75,D30,R83,U83,L12,D49,R71,U7,L72\nU62,R66,U55,R34,D71,R55,D58,R83")
    # w_one, w_two = parse_input("R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51\nU98,R91,D20,R16,D67,R40,U7,R15,U6,R7")

    bbox = boundaries(w_one, w_two)
    wiremap = mkmap(w_one, w_two, bbox)
    imshow(wiremap)
    crosses = np.where(wiremap == 45)
    crosses = [
        [cross[0] - bbox["0y"], cross[1] - bbox["0x"]]
        for cross in list(zip(crosses[0], crosses[1]))
    ]
    print(crosses)
    sums = list((abs(cross[0]) + abs(cross[1])) for cross in crosses)
    print(sums)
    print(min(sums))
