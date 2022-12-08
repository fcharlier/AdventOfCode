#!/usr/bin/python3


def read_input(filename):
    """Reads contents of filename and returns a useful data structure
    >>> heightmap = read_input("input_example")
    >>> len(heightmap)
    5
    >>> len(heightmap[0])
    5
    >>> heightmap[2][0]
    6
    >>> heightmap[3][4]
    9
    """
    with open(filename) as fd:
        return [[int(digit) for digit in line.strip()] for line in fd if len(line) > 1]


def visible(heightmap, row, col):
    """Returns true if the tree at (row, col) is visible from either top, bottom, left or right.
    Trees on the borders are always visible.
    >>> heightmap = read_input("input_example")
    >>> visible(heightmap, 1, 1)
    True
    >>> visible(heightmap, 1, 2)
    True
    >>> visible(heightmap, 1, 3)
    False
    >>> visible(heightmap, 2, 1)
    True
    >>> visible(heightmap, 2, 2)
    False
    >>> visible(heightmap, 3, 1)
    False
    >>> visible(heightmap, 3, 2)
    True
    >>> visible(heightmap, 3, 3)
    False
    """
    if (
        row == 0
        or col == 0
        or row == len(heightmap) - 1
        or col == len(heightmap[0]) - 1
    ):
        return True

    fromleft = [heightmap[row][c] < heightmap[row][col] for c in range(col)]
    fromright = [
        heightmap[row][c] < heightmap[row][col] for c in range(col + 1, len(heightmap[row]))
    ]
    fromtop = [heightmap[r][col] < heightmap[row][col] for r in range(row)]
    frombottom = [
        heightmap[r][col] < heightmap[row][col] for r in range(row + 1, len(heightmap))
    ]

    # print(f"{row},{col} <== {heightmap[row][col]}")
    # print(f"from left: {fromleft}")
    # print(f"from right: {fromright}")
    # print(f"from top: {fromtop}")
    # print(f"from bottom: {frombottom}")
    return all(fromleft) or all(fromright) or all(fromtop) or all(frombottom)


def count_visible(heightmap):
    """Count trees visible from any border
    >>> heightmap = read_input("input_example")
    >>> count_visible(heightmap)
    21
    """
    n = 0
    for row in range(len(heightmap)):
        for col in range(len(heightmap[0])):
            if visible(heightmap, row, col):
                n += 1
    return n


if __name__ == '__main__':
    heightmap = read_input("input_real")
    print(count_visible(heightmap))
