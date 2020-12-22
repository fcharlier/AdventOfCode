#!/usr/bin/env python


import functools
import itertools
import operator


def read_tiles(path):
    """Read all tiles from a file into arrays
    >>> tiles = read_tiles("example")
    >>> len(tiles)
    9
    >>> 2473 in tiles
    True
    >>> 9999 in tiles
    False
    """
    tileno = None
    tiles = {}
    with open(path) as fd:
        for line in fd.readlines():
            line = line.strip()
            if line.startswith("Tile "):
                tileno = int(line[5:-1])
                tiles[tileno] = {"name": tileno, "repr": []}
            elif line == "":
                pass
            else:
                tiles[tileno]["repr"].append(list(line))

    for tile in tiles.values():
        tile["borders"] = tile_borders(tile)
        tile["neighbors"] = {
            "top": None,
            "bottom": None,
            "left": None,
            "right": None,
        }

    return tiles


def tile_borders(tile):
    borders = {}

    borders["top"] = "".join(tile["repr"][0])
    borders["bottom"] = "".join(tile["repr"][-1])

    z = list(zip(*tile["repr"]))
    borders["left"] = "".join(z[0])[::-1]
    borders["right"] = "".join(z[-1])[::-1]

    return borders


def find_neighbors(tiles):
    bnames = ("top", "bottom", "left", "right")
    for tile, other in itertools.product(tiles.values(), tiles.values()):
        if tile["name"] != other["name"]:
            for a, b in itertools.product(bnames, bnames):
                if tile["borders"][a] in (
                    other["borders"][b],
                    other["borders"][b][::-1],
                ):
                    tile["neighbors"][a] = other["name"]
                    other["neighbors"][b] = tile["name"]


def neighbors_count(tile):
    return len([1 for v in tile["neighbors"].values() if v and v != 0])


def get_corners(tiles):
    """
    >>> tiles = read_tiles("example")
    >>> corners = get_corners(tiles)
    >>> len(corners)
    4
    >>> sorted([corner["name"] for corner in corners])
    [1171, 1951, 2971, 3079]
    >>> functools.reduce(operator.mul, (corner["name"] for corner in corners))
    20899048083289
    """
    find_neighbors(tiles)
    corners = [tile for tile in tiles.values() if neighbors_count(tile) == 2]

    return corners


if __name__ == "__main__":
    tiles = read_tiles("input")
    corners = get_corners(tiles)
    print([corner["name"] for corner in corners])
    print(functools.reduce(operator.mul, (corner["name"] for corner in corners)))
