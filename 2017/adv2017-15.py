#!/usr/bin/python
# -*- coding: utf8 -*-

# gA_first = 65
# gA_factor = 16807
gA_multiple = 4
# gB_first = 8921
# gB_factor = 48271
gB_multiple = 8
gA_first = 722
gA_factor = 16807
gB_first = 354
gB_factor = 48271

mask = 0b1111111111111111

def judge(gA, gB):
    return (gA ^ gB) & mask == 0


class Gen(object):
    def __init__(self, first, factor, multiple=1):
        self.last = first
        self.factor = factor
        self.multiple = multiple
        self.dividor = 2147483647

    def __iter__(self):
        return self

    def _build_next(self):
        return (self.last * self.factor) % self.dividor

    def next(self):
        self.last = self._build_next()
        while self.last % self.multiple != 0:
            self.last = self._build_next()
        return self.last


judge_count = 0

gA = Gen(gA_first, gA_factor, gA_multiple)
gB = Gen(gB_first, gB_factor, gB_multiple)

# print '--Gen. A--  --Gen. B--'
for n in range(5000000):
    _ga = next(gA)
    _gb = next(gB)
    # if n < 5:
    #     print '%10d  %10d' % (_ga, _gb)
    judge_count += judge(_ga, _gb)
    # if judge_count:
    #     print "Loop: %d, gA: %d, gB: %d" % (n, _ga, _gb)
    #     exit()

print "Judge count is: %d" % judge_count
