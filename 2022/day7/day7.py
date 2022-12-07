#!/usr/bin/python3

import os


def parse_input(filename):
    """Parse commands into useful structure
    >>> tree = parse_input("input_example")
    >>> len(tree["/"]["directories"])
    2
    >>> len(tree["/"]["files"])
    2
    >>> tree["/a/e"]["files"]["i"]
    584
    >>> tree["/a/e"]["size"]
    584
    >>> tree["/a"]["size"]
    94853
    >>> tree["/d"]["size"]
    24933642
    >>> tree["/"]["size"]
    48381165
    """
    curpath = []
    tree = {}
    with open(filename, encoding="utf-8") as fd:
        for line in fd:
            tokens = line.strip().split(" ")
            match tokens:
                case ["$", "cd", dirname]:
                    if dirname == "..":
                        curpath.pop()
                    else:
                        curpath.append(dirname)
                    if (path := os.path.join(*curpath)) not in tree:
                        tree[path] = {"directories": [], "files": {}, "size": 0}
                case ["$", "ls"]:
                    pass
                case ["dir", dirname]:
                    tree[path]["directories"].append(dirname)
                case [filesize, filename]:
                    tree[path]["files"][filename] = (fsz := int(filesize))
                    for n in range(len(curpath), 0, -1):
                        tree[os.path.join(*curpath[:n])]["size"] += fsz

    return tree


def at_most(tree, atmost):
    """Returns the sum of all directories which total size is at most atmost
    >>> tree = parse_input("input_example")
    >>> at_most(tree, 100000)
    95437
    """
    return sum([p["size"] for p in tree.values() if p["size"] <= 100000])


def smallest_atleast(tree, atleast):
    """Returns the size of the smallest directory which total size is at least atleast
    >>> tree = parse_input("input_example")
    >>> smallest_atleast(tree, 30000000 - (70000000 - tree["/"]["size"]))
    24933642
    """
    return min([p["size"] for p in tree.values() if p["size"] >= atleast])


if __name__ == "__main__":
    tree = parse_input("input_real")
    print("Part 1:", at_most(tree, 100000))
    print("Part 2:", smallest_atleast(tree, 30000000 - (70000000 - tree["/"]["size"])))
