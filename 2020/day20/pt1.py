#!/usr/bin/env python


import functools
import itertools
import operator
import numpy
import sys

import geom


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
    borders["left"] = "".join(z[0])
    borders["right"] = "".join(z[-1])

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


def update_neighbors(tiles, tile):
    bnames = ("top", "bottom", "left", "right")
    # Don't forget to cleanup neighbors before reassigning them
    for a in bnames:
        tile["neighbors"][a] = None

    for other in tiles.values():
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


def get_corner_tiles(tiles):
    """
    >>> tiles = read_tiles("example")
    >>> corners = get_corner_tiles(tiles)
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


def align_right_neigh(tiles, reftile, tile):
    if reftile["borders"]["right"] == tile["borders"]["left"]:
        # We're aligned already
        pass
    elif reftile["borders"]["right"] == tile["borders"]["left"][::-1]:
        # flip rows
        tile["repr"] = geom.flipRows(tile["repr"])
    elif reftile["borders"]["right"] == tile["borders"]["top"]:
        # rotate270 + flipRows
        tile["repr"] = geom.flipRows(geom.rotate270(tile["repr"]))
    elif reftile["borders"]["right"] == tile["borders"]["top"][::-1]:
        # rotate270
        tile["repr"] = geom.rotate270(tile["repr"])
    elif reftile["borders"]["right"] == tile["borders"]["right"]:
        # rotate180 then flipRows
        tile["repr"] = geom.flipRows(geom.rotate180(tile["repr"]))
    elif reftile["borders"]["right"] == tile["borders"]["right"][::-1]:
        # rotate 180
        tile["repr"] = geom.rotate180(tile["repr"])
    elif reftile["borders"]["right"] == tile["borders"]["bottom"]:
        # rotate90
        tile["repr"] = geom.rotate90(tile["repr"])
    elif reftile["borders"]["right"] == tile["borders"]["bottom"][::-1]:
        # rotate90 then flipRows
        tile["repr"] = geom.flipRows(geom.rotate90(tile["repr"]))

    tile["borders"] = tile_borders(tile)
    update_neighbors(tiles, tile)


def align_bottom_neigh(tiles, reftile, tile):
    if reftile["borders"]["bottom"] == tile["borders"]["top"]:
        # We're aligned already
        pass
    elif reftile["borders"]["bottom"] == tile["borders"]["top"][::-1]:
        # flip rows
        tile["repr"] = geom.flipCols(tile["repr"])
    elif reftile["borders"]["bottom"] == tile["borders"]["left"]:
        # rotate90 + flipCols
        tile["repr"] = geom.flipCols(geom.rotate90(tile["repr"]))
    elif reftile["borders"]["bottom"] == tile["borders"]["left"][::-1]:
        # rotate90
        tile["repr"] = geom.rotate90(tile["repr"])
    elif reftile["borders"]["bottom"] == tile["borders"]["right"]:
        # rotate270
        tile["repr"] = geom.rotate270(tile["repr"])
    elif reftile["borders"]["bottom"] == tile["borders"]["right"][::-1]:
        # rotate 270 then flipCols
        tile["repr"] = geom.flipCols(geom.rotate270(tile["repr"]))
    elif reftile["borders"]["bottom"] == tile["borders"]["bottom"]:
        # rotate180 then flipCols
        tile["repr"] = geom.flipCols(geom.rotate180(tile["repr"]))
    elif reftile["borders"]["bottom"] == tile["borders"]["bottom"][::-1]:
        # rotate180
        tile["repr"] = geom.rotate180(tile["repr"])

    tile["borders"] = tile_borders(tile)
    update_neighbors(tiles, tile)


def align_all_to_right(tiles, start):
    reftile = start
    while reftile["neighbors"]["right"]:
        align_right_neigh(tiles, reftile, tiles[reftile["neighbors"]["right"]])
        reftile = tiles[reftile["neighbors"]["right"]]

    if start["neighbors"]["bottom"]:
        bottom = tiles[start["neighbors"]["bottom"]]
        align_bottom_neigh(tiles, start, bottom)
        align_all_to_right(tiles, bottom)


def verify_all(tiles):
    dirs = (
        ("top", "bottom"),
        ("bottom", "top"),
        ("left", "right"),
        ("right", "left"),
    )
    for tile in tiles.values():
        for a, b in dirs:
            neigh = tile["neighbors"][a]
            if neigh:
                neigh = tiles[neigh]
                assert tile["borders"][a] == neigh["borders"][b]


def remove_borders(tiles):
    def c_to_int(c):
        if c == "#":
            return 1
        else:
            return 0

    for tile in tiles.values():
        tile["noframe"] = [
            [c_to_int(c) for c in line[1:-1]] for line in tile["repr"][1:-1]
        ]
    return numpy.array(tile["noframe"]).shape


def make_image(tiles, tile_shape, topleft):
    start = topleft
    tileW, tileH = tile_shape

    numpy.set_printoptions(threshold=sys.maxsize, linewidth=300)

    # Get number of tiles along width
    tile = start["name"]
    n = 0
    while tile:
        n += 1
        tile = tiles[tile]["neighbors"]["right"]
    ntiles_w = n

    # Get number of tiles along height
    tile = start["name"]
    n = 0
    while tile:
        n += 1
        tile = tiles[tile]["neighbors"]["bottom"]
    ntiles_h = n

    # Create destination image
    image_shape = ntiles_w * tileW, ntiles_h * tileH
    image = numpy.ndarray(image_shape, dtype=int)

    x, y = 0, 0
    row = start["name"]
    while row:  # Columns
        col = row
        x = 0
        while col:  # Rows
            image[y * tileH : y * tileH + tileH, x * tileW : x * tileW + tileW] = tiles[
                col
            ]["noframe"]

            col = tiles[col]["neighbors"]["right"]
            x += 1

        row = tiles[row]["neighbors"]["bottom"]
        y += 1

    return image


def get_monster():
    monster = "                  # ;" "#    ##    ##    ###;" " #  #  #  #  #  #   "
    monster = monster.translate(monster.maketrans(" #", "01"))
    monster = " ".join(list(monster))
    arr = numpy.array(numpy.mat(monster), dtype=int)

    return arr


def as_examples(im):
    X, Y = im.shape
    for x in range(X):
        for y in range(Y):
            if im[x, y] == 1:
                print("#", end="")
            else:
                print(".", end="")
        print()


def find_monster(image, monster):
    count = 0
    X, Y = image.shape
    mX, mY = monster.shape
    for y in range(0, Y - mY):
        for x in range(0, X - mX):
            xtract = image[x : x + mX, y : y + mY]

            if numpy.array_equal(numpy.logical_or(xtract, monster), xtract):
                count += 1

    if count:
        nz_im = numpy.count_nonzero(image)
        nz_monster = numpy.count_nonzero(monster) * count
        return nz_im - nz_monster

    return 0


def turn_it_around(image, monster):
    """
    >>> tiles = read_tiles("example")
    >>> corners = get_corner_tiles(tiles)
    >>> topleft = [ c for c in corners if c["neighbors"]["bottom"] and c["neighbors"]["right"] ][0]
    >>> align_all_to_right(tiles, topleft)
    >>> verify_all(tiles)
    >>> shp = remove_borders(tiles)
    >>> image = make_image(tiles, shp, topleft)
    >>> turn_it_around(image, get_monster())
    273
    """
    for rot in range(4):
        bleh = numpy.rot90(image, rot)
        roughness = find_monster(bleh, monster)
        if roughness:
            return roughness
        bleh = numpy.flipud(numpy.rot90(image, rot))
        roughness = find_monster(bleh, monster)
        if roughness:
            return roughness
        bleh = numpy.fliplr(numpy.rot90(image, rot))
        roughness = find_monster(bleh, monster)
        if roughness:
            return roughness


if __name__ == "__main__":
    tiles = read_tiles("input")
    corners = get_corner_tiles(tiles)
    print("Corners are:", [corner["name"] for corner in corners])
    print(
        "Part 1 answer:",
        functools.reduce(operator.mul, (corner["name"] for corner in corners)),
    )

    topleft = [
        c for c in corners if c["neighbors"]["bottom"] and c["neighbors"]["right"]
    ][0]

    align_all_to_right(tiles, topleft)
    verify_all(tiles)
    shp = remove_borders(tiles)

    im = make_image(tiles, shp, topleft)
    monster = get_monster()
    roughness = turn_it_around(im, monster)
    print(f"Habitat's water roughness is: {roughness}.")
