#!/usr/bin/env python

import numpy as np


def read_input(filename):
    """
    >>> c, f = read_input('example')
    >>> len(c)
    18
    >>> len(f)
    2
    >>> f[0]
    ('y', 7)
    """
    coords = []
    folds = []
    with open(filename) as fd:
        for line in fd:
            if "," in line:
                x, y = line.strip().split(",")
                coords.append((int(y), int(x)))
            elif "fold along" in line:
                line = line.replace("fold along ", "")
                axis, n = line.strip().split("=")
                folds.append((axis, int(n)))
    return coords, folds


def build_paper(coords):
    """
    >>> ppr = build_paper(read_input('example')[0])
    >>> ppr.shape
    (15, 11)
    >>> np.size(ppr[ppr == True])
    18
    """
    clists = tuple(zip(*coords))
    paper = np.zeros((max(clists[0]) + 1, max(clists[1]) + 1), dtype=np.bool_)
    paper[clists] = True
    return paper


def fold_along(paper, fold_axis, fold_where):
    """
    >>> dots, folds = read_input('example')
    >>> paper = build_paper(dots)
    >>> paper = fold_along(paper, *folds[0])
    >>> paper.shape
    (7, 11)
    >>> np.size(paper[paper == True])
    17
    >>> paper = fold_along(paper, *folds[1])
    >>> paper.shape
    (7, 5)
    >>> np.size(paper[paper == True])
    16
    """
    if fold_axis == "y":
        top = paper[0:fold_where, :]
        bottom = paper[fold_where + 1 :, :]
        # pad the bottom part when the fold doesn't yield enought rows
        if bottom.shape[0] < top.shape[0]:
            bottom = np.pad(bottom, ((0, 1), (0, 0)), "constant", constant_values=False)
        return top | np.flipud(bottom)
    elif fold_axis == "x":
        left = paper[:, 0:fold_where]
        right = paper[:, fold_where + 1 :]
        # pad the right part when the fold doesn't yield enought columns
        if right.shape[1] < left.shape[1]:
            right = np.pad(right, ((0, 0), (0, 1)), "constant", constant_values=False)
        return left | np.fliplr(right)


def display_paper(paper):
    for y in range(paper.shape[0]):
        for x in range(paper.shape[1]):
            if paper[y, x]:
                print("█", end="")
            else:
                print("░", end="")
        print("")


if __name__ == "__main__":
    dots, folds = read_input("input")
    paper = build_paper(dots)
    paper = fold_along(paper, *folds[0])
    print("Part 1: ", np.size(paper[paper == True]))
    for fold in folds[1:]:
        paper = fold_along(paper, *fold)
    print("Part 2:")
    display_paper(paper)
