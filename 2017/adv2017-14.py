#!/usr/bin/env python
# -*- coding: utf-8 -*-

from operator import xor
import pprint
from string import maketrans


def knot_hash_strong(pzl, elts=range(256)):
    pzl = map(ord, (a for a in pzl))
    pzl = pzl + [17, 31, 73, 47, 23]
    # print pzl
    skip = 0
    pos = 0
    count = 0

    for _ in xrange(64):
        count += 1
        for length in pzl:
            end = pos + length

            if end < len(elts):
                left = elts[0:pos]
                rev = elts[pos:end]
                mid = rev[::-1]
                right = elts[end:len(elts)]
            else:
                end = end % len(elts)
                rev = elts[pos:len(elts)] + elts[0:end]
                rev = rev[::-1]
                left = rev[length - end:]
                mid = elts[end:pos]
                right = rev[0:length - end]

            elts = left + mid + right
            pos = (pos + length + skip) % len(elts)
            skip += 1

    # print count
    dense_hash = []
    for n in xrange(16):
        xor16 = reduce(xor, elts[n*16:n*16+16])
        dense_hash.append(xor16)

    result = ''.join(format(x, "08b") for x in dense_hash)
    return result


def mark_adjacent(hashes, group, row, col):
    if row >= 0 and row < 128 and col >= 0 and col < 128:
        if hashes[row][col] == '#':
            hashes[row][col] = group
            mark_adjacent(hashes, group, row - 1, col)
            mark_adjacent(hashes, group, row + 1, col)
            mark_adjacent(hashes, group, row, col - 1)
            mark_adjacent(hashes, group, row, col + 1)


# puzzle = 'flqrgnkx'
puzzle = 'hfdlxzhv'
hashes = []
transtab = maketrans('01', '.#')

for n in range(128):
    h = knot_hash_strong("%s-%d" % (puzzle, n))
    h = h.translate(transtab)
    h = list(h)
    hashes.append(h)


used = sum(sum([1 for c in h if c == '#']) for h in hashes)
print "Used: %d" % used


next_group = 1
for row in range(128):
    for col in range(128):
        if hashes[row][col] == '#':
            mark_adjacent(hashes, next_group, row, col)
            next_group += 1

print "Groups found: %d" % (next_group - 1)
