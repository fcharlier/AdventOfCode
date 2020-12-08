#!/usr/bin/python

from operator import xor

puzzle_input = (70, 66, 255, 2, 48, 0, 54, 48, 80, 141, 244, 254, 160, 108, 1,
                41)


puzzle_input_strong = '70,66,255,2,48,0,54,48,80,141,244,254,160,108,1,41'


def disp(l, paren=False):
    if paren:
        print '(',
    for n in range(len(l)):
        print l[n],
    if paren:
        print ')',


def knot_hash(pzl, elts=range(256)):
    pos = 0
    for skip, length in enumerate(pzl):
        end = pos + length

        if end < len(elts):
            left = elts[0:pos]
            rev = elts[pos:end]
            mid = rev[::-1]
            right = elts[end:len(elts)]

            # disp(left)
            # disp(rev, True)
            # disp(right)
            # print '-->',
            # disp(left)
            # disp(mid, True)
            # disp(right)
            # print
        else:
            end = end % len(elts)
            rev = elts[pos:len(elts)] + elts[0:end]
            rev = rev[::-1]
            left = rev[length - end:]
            mid = elts[end:pos]
            right = rev[0:length - end]

        elts = left + mid + right
        # print "Skip: %d - Pos: %d" % (skip, pos)
        pos = (pos + length + skip) % len(elts)

    return elts[0] * elts[1]


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

    result = ''.join("%x" % x for x in dense_hash)
    return result


if __name__ == '__main__':
    print knot_hash((3, 4, 1, 5), (0, 1, 2, 3, 4))
    print knot_hash(puzzle_input)
    # print knot_hash_strong("3,4,1,5,17,31,73,47,23", (0, 1, 2, 3, 4))
    print knot_hash_strong("")
    print knot_hash_strong("AoC 2017")
    print knot_hash_strong("1,2,3")
    print knot_hash_strong("1,2,4")
    print knot_hash_strong(puzzle_input_strong)
