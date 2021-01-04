#!/usr/bin/env python

import numpy as np
import scipy.ndimage

SE = np.array([0, -1, 1])
SW = np.array([-1, 0, 1])
E = np.array([1, -1, 0])
W = np.array([-1, 1, 0])
NE = np.array([1, 0, -1])
NW = np.array([0, 1, -1])

D = [SE, SW, E, W, NE, NW]


def coords_from_path(tile_path):
    """Meh
    >>> coords_str(coords_from_path("esew"))
    '0,-1,1'
    >>> coords_str(coords_from_path("nwwswee"))
    '0,0,0'
    """
    dirs = {}
    for d in ("se", "sw", "nw", "ne", "w", "e"):
        dirs[d] = tile_path.count(d)
        tile_path = tile_path.replace(d, d.upper())

    v = (
        dirs["se"] * SE
        + dirs["ne"] * NE
        + dirs["sw"] * SW
        + dirs["nw"] * NW
        + dirs["e"] * E
        + dirs["w"] * W
    )
    return v


def coords_str(coords):
    return ",".join(str(c) for c in coords)


def step(grid):
    # grid = np.pad(grid, 1)

    # Build our convolution kernel
    k = np.zeros((3, 3, 3), dtype=np.byte)
    for d in D:
        k[d[0] + 1, d[1] + 1, d[2] + 1] = 1

    counts = scipy.ndimage.convolve(grid, k, mode="constant", cval=0)
    blacks = set(tuple(c) for c in np.argwhere(grid == 1))
    whites = set(tuple(c) for c in np.argwhere(grid == 0))

    towhite = (
        set(tuple(c) for c in np.argwhere(counts == 0))
        | set(tuple(c) for c in np.argwhere(counts > 2)) & blacks
    )
    toblack = set(tuple(c) for c in np.argwhere(counts == 2)) & whites

    for idx in towhite:
        grid[idx] = 0

    for idx in toblack:
        grid[idx] = 1

    return grid


def strip(grid):
    blacks_indexes = np.nonzero(grid)
    miX, miY, miZ = (min(dim) for dim in blacks_indexes)
    maX, maY, maZ = (max(dim) + 1 for dim in blacks_indexes)

    return grid[miX:maX, miY:maY, miZ:maZ]


def main(filepath, days=100):
    """This time I don't want to do complicated math required if I only stored only the
    positions of black tiles (although it would be much faster than building the grid).
    Finds the final solution in 7:46,68 examples in 2:15 on a Intel(R) Core(TM) i5 CPU
    750 @ 2.67GHz.
    >>> main("EXAMPLE", 10)
    37
    >>> main("EXAMPLE", 20)
    132
    >>> main("EXAMPLE", 30)
    259
    >>> main("EXAMPLE", 100)
    2208
    """
    with open(filepath) as fd:
        paths = [li.strip() for li in fd.readlines()]

    # Get the tiles coordinates
    tiles_coords = [coords_from_path(p) for p in paths]

    # Change origin to have only coordinates >= 0
    minX = min(t[0] for t in tiles_coords)
    minY = min(t[1] for t in tiles_coords)
    minZ = min(t[2] for t in tiles_coords)
    minC = np.array([minX, minY, minZ])

    tiles_coords = [t - minC for t in tiles_coords]

    maxX = max(t[0] for t in tiles_coords)
    maxY = max(t[1] for t in tiles_coords)
    maxZ = max(t[2] for t in tiles_coords)
    grid = np.zeros((maxX + 1, maxY + 1, maxZ + 1), dtype=np.byte)

    for t in tiles_coords:
        if grid[t[0], t[1], t[2]] == 0:
            grid[t[0], t[1], t[2]] = 1
        else:
            grid[t[0], t[1], t[2]] = 0

    for _ in range(days):
        grid = strip(grid)
        grid = np.pad(grid, 1)
        grid = step(grid)

    return np.count_nonzero(grid)


if __name__ == "__main__":
    print(main("INPUT"))
