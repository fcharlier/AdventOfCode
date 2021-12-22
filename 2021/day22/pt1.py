#!/usr/bin/env python

import numpy as np
import re


def read_input(filename):
    """
    >>> orders = read_input('example')
    >>> len(orders)
    22
    >>> orders[0]
    (True, (-20, 26), (-36, 17), (-47, 7))
    >>> orders[21]
    (True, (967, 23432), (45373, 81175), (27513, 53682))
    """
    rex = re.compile(
        r"^(?P<order>on|off) x=(?P<x0>-?\d+)\.\.(?P<x1>-?\d+),"
        r"y=(?P<y0>-?\d+)\.\.(?P<y1>-?\d+),"
        r"z=(?P<z0>-?\d+)\.\.(?P<z1>-?\d+)$"
    )
    orders = []
    with open(filename) as fdesc:
        for line in fdesc:
            m = rex.match(line.strip())
            orders.append(
                (
                    m["order"] == "on",
                    (int(m["x0"]), int(m["x1"])),
                    (int(m["y0"]), int(m["y1"])),
                    (int(m["z0"]), int(m["z1"])),
                )
            )
    return orders


def out_of_range(axis, lower, upper):
    return axis[0] > upper or axis[1] < lower


def shift_clip(axis, shift=50, lower=0, upper=100):
    return max(axis[0] + 50, lower), min(axis[1] + 50, upper)


def filter_orders(orders):
    """
    >>> orders = filter_orders(read_input('example'))
    >>> len(orders)
    20
    """
    new_orders = []
    for order, X, Y, Z in orders:
        # This is outside of our zone of interest
        if (
            out_of_range(X, -50, 50)
            or out_of_range(Y, -50, 50)
            or out_of_range(Z, -50, 50)
        ):
            continue

        # Limit to 0..100 for every axis
        new_orders.append((order, shift_clip(X), shift_clip(Y), shift_clip(Z)))
    return new_orders


def apply_orders(orders):
    """
    >>> cube = apply_orders(read_input('example0'))
    >>> len(cube[cube == True])
    39
    >>> cube = apply_orders(filter_orders(read_input('example')))
    >>> len(cube[cube == True])
    590784
    """
    reactor = np.ndarray((101, 101, 101), dtype=np.bool_)
    reactor.fill(False)

    for order, X, Y, Z in orders:
        reactor[Z[0] : Z[1] + 1, Y[0] : Y[1] + 1, X[0] : X[1] + 1] = order

    return reactor


if __name__ == "__main__":
    cube = apply_orders(filter_orders(read_input("input")))
    print(len(cube[cube == True]))
