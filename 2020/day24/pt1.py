#!/usr/bin/env python

import numpy as np


def coords_from_path(tile_path):
    """Meh
    >>> coords_from_path("esew")
    '0,-1,1'
    >>> coords_from_path("nwwswee")
    '0,0,0'
    """
    dirs = {}
    for d in ("se", "sw", "nw", "ne", "w", "e"):
        dirs[d] = tile_path.count(d)
        tile_path = tile_path.replace(d, d.upper())

    se = np.array([0, -1, 1])
    sw = np.array([-1, 0, 1])
    e = np.array([1, -1, 0])
    w = np.array([-1, 1, 0])
    ne = np.array([1, 0, -1])
    nw = np.array([0, 1, -1])

    v = (
        dirs["se"] * se
        + dirs["ne"] * ne
        + dirs["sw"] * sw
        + dirs["nw"] * nw
        + dirs["e"] * e
        + dirs["w"] * w
    )
    return ",".join(str(c) for c in v)


def main(filepath):
    """
    >>> main("EXAMPLE")
    10
    """
    with open(filepath) as fd:
        paths = [li.strip() for li in fd.readlines()]

    tiles = [coords_from_path(p) for p in paths]
    black_tiles = [t for t in set(tiles) if tiles.count(t) % 2 != 0]
    return len(black_tiles)


if __name__ == "__main__":
    print(main("INPUT"))
