#!/usr/bin/python3

with open("input_real") as fd:
    work = [[list(map(int, work.split("-"))) for work in line.strip().split(",")] for line in fd.readlines() ]


contained = 0
for (worka, workb) in work:
    if worka[0] >= workb[0] and worka[1] <=workb[1]:
        contained += 1
    elif workb[0] >= worka[0] and workb[1] <= worka[1]:
        contained += 1
print(contained)
