#!/usr/bin/env python

import cmath
import math
import time


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
    print("\x1b[2J")
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
    # viewable = []
    # # show(data)
    # marker = 0
    # for y in range(len(data)):
    #     for x in range(len(data[y])):
    #         if data[y][x] != "." and not (x == X and y == Y):
    #             # print("Inspecting (%d, %d):%s" % (x, y, data[y][x]))
    #             v = V(x - X, y - Y)
    #             # print(v)
    #             hides = is_hidden(v, viewable)
    #             if hides:
    #                 # data[y][x] = "%"
    #                 pass
    #             else:
    #                 viewable.append(v)
    #                 # data[y][x] = chr(ord("A") + marker)
    #                 marker += 1
    #
    # # show(data)
    # return len(viewable)
    return len(byPhase(data, X, Y))


def locateLaser(data):
    for y in range(len(data)):
        for x in range(len(data[y])):
            if data[y][x] == "X":
                return (x, y)


def byPhase(data, X, Y):
    """Identifies asteroid and stores them by phase"""
    asteroids = {}

    for y in range(len(data)):
        for x in range(len(data[y])):
            if data[y][x] != "." and not (x == X and y == Y):
                angle = cmath.phase(complex(-y + Y, x - X))
                if angle < 0.:
                    angle += 2 * math.pi
                if angle not in asteroids:
                    asteroids[angle] = []
                asteroids[angle].append((x - X, y - Y))

    sorted_asteroids = {}
    for phase, asts in asteroids.items():
        _list = sorted(asts, key=lambda asteroid: abs(complex(*asteroid)))
        _list.reverse()
        sorted_asteroids[str(phase)] = _list

    return sorted_asteroids


def doit(data):
    maxime = 0
    pos_maxime = None
    # show(data)
    for y in range(len(data)):
        for x in range(len(data[y])):
            if data[y][x] != ".":
                # data[y][x] = canview(data, x, y)
                viewed = canview(data.copy(), x, y)
                if viewed > maxime:
                    maxime = viewed
                    pos_maxime = (x, y)
    return maxime, pos_maxime


def destroy(data, laser, byphase):
    phases = sorted(byphase.keys(), key=float)
    # show(data)
    counter = 0
    while True:
        for phase in phases:
            if phase in byphase and byphase[phase] and len(byphase[phase]) > 0:
                counter += 1
                destroyed = byphase[phase].pop()
                X = destroyed[0] + laser[0]
                Y = destroyed[1] + laser[1]
                data[Y][X] = "*"
                # show(data)
                if counter in (1, 2, 3, 10, 20, 50, 100, 199, 200, 201, 299):
                    print("%d: %d,%d" % (counter, X, Y))
                    if counter >= 200:
                        return X * 100 + Y


if __name__ == "__main__":
    with open("data") as data:
        data = [list(line.strip()) for line in data.readlines()]

    # laser = locateLaser(data)
    maxime, laser = doit(data)
    print("Maximum: %d found at %d,%d" % (maxime, *laser))
    byphase = byPhase(data, *laser)
    answer = destroy(data, laser, byphase)
    print("Answer is: %d" % answer)
