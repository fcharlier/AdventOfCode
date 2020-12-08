#!/usr/bin/python

puzzle = [11, 11, 13, 7, 0, 15, 5, 5, 4, 4, 1, 1, 7, 1, 15, 11]
# puzzle = [0, 2, 7, 0]


seen = ['.'.join(map(str, puzzle))]
step = 0
while True:
    step += 1

    cell = max(enumerate(puzzle), key=lambda x: x[1])[0]
    print "Puzzle: %s" % puzzle
    print "Selected: %d" % cell
    amount = puzzle[cell]
    puzzle[cell] = 0
    while amount > 0:
        cell = (cell + 1) % len(puzzle)
        puzzle[cell] += 1
        amount -= 1

    view = '.'.join(map(str, puzzle))
    if view in seen:
        print step
        break
    seen.append(view)

puzzle = [11, 11, 13, 7, 0, 15, 5, 5, 4, 4, 1, 1, 7, 1, 15, 11]
# puzzle = [0, 2, 7, 0]

step = 0
seen = {'.'.join(map(str, puzzle)): step}
while True:
    step += 1

    cell = max(enumerate(puzzle), key=lambda x: x[1])[0]
    print "Puzzle: %s" % puzzle
    print "Selected: %d" % cell
    amount = puzzle[cell]
    puzzle[cell] = 0
    while amount > 0:
        cell = (cell + 1) % len(puzzle)
        puzzle[cell] += 1
        amount -= 1

    view = '.'.join(map(str, puzzle))
    if view in seen:
        print step - seen[view]
        break
    seen[view] = step
