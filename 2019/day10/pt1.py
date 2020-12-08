#!/usr/bin/env python


class V(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "%+03d %+03d" % (self.x, self.y)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return (
            self.x * other.x >= 0 and self.y * other.y >= 0 and self.x * other.y == other.x * self.y
        )


def is_hidden(v, viewable):
    for _v in viewable:
        if v == _v:
            return _v
    return False


def show(data):
    for y in range(len(data)):
        for x in range(len(data[y])):
            print(data[y][x], end="")
        print("")


def canview(data, X, Y):
    """Returns the number of items viewable from the X,Y point

    >>> canview([['.', '#', '.', '.', '#'],
    ... ['.', '.', '.', '.', '.'],
    ... ['#', '#', '#', '#', '#'],
    ... ['.', '.', '.', '.', '#'],
    ... ['.', '.', '.', '#', '#']], 3, 4)
    8
    >>> canview([['.', '.', '.', '.', '.', '.', '#', '.', '#', '.'],
    ... ['#', '.', '.', '#', '.', '#', '.', '.', '.', '.'],
    ... ['.', '.', '#', '#', '#', '#', '#', '#', '#', '.'],
    ... ['.', '#', '.', '#', '.', '#', '#', '#', '.', '.'],
    ... ['.', '#', '.', '.', '#', '.', '.', '.', '.', '.'],
    ... ['.', '.', '#', '.', '.', '.', '.', '#', '.', '#'],
    ... ['#', '.', '.', '#', '.', '.', '.', '.', '#', '.'],
    ... ['.', '#', '#', '.', '#', '.', '.', '#', '#', '#'],
    ... ['#', '#', '.', '.', '.', '#', '.', '.', '#', '.'],
    ... ['.', '#', '.', '.', '.', '.', '#', '#', '#', '#']], 5, 8)
    33
    >>> canview([['#', '.', '#', '.', '.', '.', '#', '.', '#', '.'],
    ... ['.', '#', '#', '#', '.', '.', '.', '.', '#', '.'],
    ... ['.', '#', '.', '.', '.', '.', '#', '.', '.', '.'],
    ... ['#', '#', '.', '#', '.', '#', '.', '#', '.', '#'],
    ... ['.', '.', '.', '.', '#', '.', '#', '.', '#', '.'],
    ... ['.', '#', '#', '.', '.', '#', '#', '#', '.', '#'],
    ... ['.', '.', '#', '.', '.', '.', '#', '#', '.', '.'],
    ... ['.', '.', '#', '#', '.', '.', '.', '.', '#', '#'],
    ... ['.', '.', '.', '.', '.', '.', '#', '.', '.', '.'],
    ... ['.', '#', '#', '#', '#', '.', '#', '#', '#', '.']], 1, 2)
    35
    """
    viewable = []
    # show(data)
    marker = 0
    for y in range(len(data)):
        for x in range(len(data[y])):
            if data[y][x] != "." and not (x == X and y == Y):
                # print("Inspecting (%d, %d):%s" % (x, y, data[y][x]))
                v = V(x - X, y - Y)
                # print(v)
                hides = is_hidden(v, viewable)
                if hides:
                    # data[y][x] = "%"
                    pass
                else:
                    viewable.append(v)
                    # data[y][x] = chr(ord("A") + marker)
                    marker += 1

    # show(data)
    return len(viewable)


def doit(data):
    maxime = 0
    # show(data)
    for y in range(len(data)):
        for x in range(len(data[y])):
            if data[y][x] != ".":
                # data[y][x] = canview(data, x, y)
                maxime = max(maxime, canview(data.copy(), x, y))
    return maxime


if __name__ == "__main__":
    with open("data") as data:
        data = [list(line.strip()) for line in data.readlines()]

    print(doit(data))
