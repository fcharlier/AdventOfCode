#!/usr/bin/python3

with open("input_real") as fd:
    work = [[list(map(int, work.split("-"))) for work in line.strip().split(",")] for line in fd.readlines() ]


overlaps = 0
for (worka, workb) in work:
    if worka[0] < workb[0]:
        worka, workb = workb, worka

    if worka[0] <= workb[1]:
        overlaps += 1

print(overlaps)
