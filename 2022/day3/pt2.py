# coding: utf-8
remains = []
with open("input_real") as fd:
    rucksacks = fd.readlines()


def ltrprio(ltr):
    if ltr.islower():
        return ord(ltr) - ord("a") + 1
    else:
        return ord(ltr) - ord("A") + 27


for n in range(0, len(rucksacks) - 1, 3):
    rs1 = set(rucksacks[n].strip())
    rs2 = set(rucksacks[n + 1].strip())
    rs3 = set(rucksacks[n + 2].strip())
    remains.append((rs1 & rs2 & rs3).pop())

print(sum([ltrprio(l) for l in remains]))
