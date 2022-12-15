#!/usr/bin/python3

import re
import sys


def manhatan_distance(p1, p2):
    """
    >>> manhatan_distance((0, 0), (1, 0))
    1
    >>> manhatan_distance((0, 0), (1, 1))
    2
    >>> manhatan_distance((0, 0), (10, 20))
    30
    >>> manhatan_distance((-10, 0), (10, 0))
    20
    >>> manhatan_distance((2, 18), (-2, 15))
    7
    """
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def read_input(filename):
    """
    >>> sensors = read_input("input_example")
    >>> len(sensors)
    14
    >>> sensors[0]["loc"]
    (2, 18)
    >>> sensors[0]["beacon"]
    (-2, 15)
    >>> sensors[0]["range"]
    7
    >>> sensors[13]["loc"]
    (20, 1)
    >>> sensors[13]["beacon"]
    (15, 3)
    >>> sensors[13]["range"]
    7
    """
    pattern = re.compile(
        r"Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)"
    )
    with open(filename) as fd:
        report_data = pattern.findall(fd.read())
    sensors = []
    for coords in report_data:
        (sx, sy, bx, by) = tuple(map(int, coords))
        sensors.append(
            {
                "loc": (sx, sy),
                "beacon": (bx, by),
                "range": manhatan_distance((sx, sy), (bx, by)),
            }
        )
    return sensors


def shape(sensors):
    """
    >>> sensors = read_input("input_example")
    >>> shape(sensors)
    ((-8, -10), (28, 26))
    """
    minX, minY, maxX, maxY = (sys.maxsize, sys.maxsize, 0, 0)
    for sensor in sensors:
        minX = min(minX, sensor["loc"][0] - sensor["range"])
        minY = min(minY, sensor["loc"][1] - sensor["range"])
        maxX = max(maxX, sensor["loc"][0] + sensor["range"])
        maxY = max(maxY, sensor["loc"][1] + sensor["range"])
    return ((minX, minY), (maxX, maxY))


def count_no_beacon(sensors, line_no):
    """
    >>> sensors = read_input("input_example")
    >>> count_no_beacon(sensors, 10)
    26
    """
    ((minX, minY), (maxX, maxY)) = shape(sensors)
    y = line_no
    no_beacon = 0
    for x in range(minX, maxX + 1):
        is_in_range = False
        is_beacon = False
        for sensor in sensors:
            if (x, y) == sensor["beacon"]:
                is_beacon = True
                break
        if not is_beacon:
            for sensor in sensors:
                if manhatan_distance((x, y), sensor["loc"]) <= sensor["range"]:
                    is_in_range = True
                    break
            if is_in_range:
                no_beacon += 1

    return no_beacon


if __name__ == '__main__':
    sensors = read_input("input_real")
    print(count_no_beacon(sensors, 2000000))
