#!/usr/bin/python3

import re


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


def merge_scan(scans, new):
    newranges = []

    for scan in scans:
        if (
            scan[0] <= new[0] + 1 <= scan[1]
            or scan[0] <= new[1] + 1 <= scan[1]
            or new[0] <= scan[0] + 1 <= new[1]
            or new[0] <= scan[1] + 1 <= new[1]
        ):
            new = (min(scan[0], new[0]), max(scan[1], new[1]))
        else:
            newranges.append(scan)

    newranges.append(new)
    return newranges


def distress_frequency(sensors, maxrange=(0, 4000000)):
    """
    >>> sensors = read_input("input_example")
    >>> distress_frequency(sensors, maxrange=(0,20))
    56000011
    """
    (minX, maxX) = maxrange
    (minY, maxY) = maxrange

    for row in range(minY, maxY + 1):
        scanned = []
        for sensor in sensors:
            if (remain := (sensor["range"] - abs(sensor["loc"][1] - row))) > 0:
                scan = (
                    max(sensor["loc"][0] - remain, minX),
                    min(sensor["loc"][0] + remain, maxX),
                )
                scanned = merge_scan(scanned, scan)
        if len(scanned) == 2:
            scanned = sorted(scanned, key=lambda r: r[0])
            return (scanned[0][1] + 1) * 4000000 + row

    return "FAILED"


if __name__ == "__main__":
    sensors = read_input("input_real")
    print(distress_frequency(sensors))
