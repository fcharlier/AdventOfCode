# coding: utf-8
with open("input_real") as fd:
    rucksacks = fd.readlines()
    
remains = []
for rucksack in rucksacks:
    rucksack = rucksack.strip()
    if not rucksack:
        next
    c1, c2 = set(rucksack[0:int(len(rucksack)/2)]), set(rucksack[int(len(rucksack)/2):])
    remains.append((c1&c2).pop())
    
sum([ltrprio(l) for l in remains])
