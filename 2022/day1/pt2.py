#!/usr/bin/python3

with open("data_real", "r") as fd:
    curcal = 0
    cals = []
    for line in fd:
        if line.strip():
            curcal += int(line.strip())
        else:
            cals.append(curcal)
            curcal = 0
    cals.append(curcal)

print(sum(sorted(cals)[-3:]))
