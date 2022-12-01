#!/usr/bin/python3

with open("data_real", "r") as fd:
    curcal = 0
    maxcal = 0
    for line in fd:
        if line.strip():
            curcal += int(line.strip())
        else:
            maxcal = max(curcal, maxcal)
            curcal = 0
    maxcal = max(curcal, maxcal)

print(maxcal)
