#!/usr/bin/env python3

from anytree import Node, findall, find_by_attr, RenderTree, AsciiStyle
from anytree.util import commonancestors


def readmap(orbitmap):
    """Reads an orbit map"""
    COM = None
    ERRANDS = Node("--ERRAND--")

    for orbit in orbitmap:
        center, orbiter = orbit.strip().split(")")

        if center == "COM":
            COM = Node(center)

        centerNode = None
        if COM:
            centerNode = find_by_attr(COM, center)
        if centerNode is None:
            centerNode = find_by_attr(ERRANDS, center)
        if centerNode is None:
            centerNode = Node(center, parent=ERRANDS)

        orbiterNode = find_by_attr(ERRANDS, orbiter)
        if orbiterNode is not None:
            orbiterNode.parent = centerNode
        else:
            orbiterNode = Node(orbiter, parent=centerNode)

    return COM


def verifymap(orbitmap):
    """Verifies an orbitmap, returns the checksum
    >>> verifymap(readmap("COM)B\\nB)C\\nC)D\\nD)E\\nE)F\\nB)G\\nG)H\\nD)I\\nE)J\\nJ)K\\nK)L"))
    42
    """
    count = 0
    orbiters = findall(orbitmap, filter_=lambda node: node.name != "COM")
    for orbiter in orbiters:
        count += orbiter.depth

    return count


if __name__ == "__main__":
    with open("data") as data:
        orbitmap = data.readlines()
    orbitmap = readmap(orbitmap)

    YOU = find_by_attr(orbitmap, "YOU")
    SAN = find_by_attr(orbitmap, "SAN")

    ancestors = commonancestors(YOU.parent, SAN.parent)
    print(
        "To move from YOU's parent to SAN's parent requires: %d"
        % (YOU.parent.depth + SAN.parent.depth - 2 * ancestors[-1].depth)
    )
