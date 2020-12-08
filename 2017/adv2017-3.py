#!/usr/bin/python

import pprint


def side_len(ring):
    """
    >>> side_len(0)
    1
    >>> side_len(1)
    2
    >>> side_len(2)
    4
    >>> side_len(3)
    6
    """
    if ring == 0:
        return 1
    else:
        return ring * 2


def contour_len(ring):
    """
    >>> contour_len(0)
    1
    >>> contour_len(1)
    8
    >>> contour_len(2)
    16
    >>> contour_len(3)
    24
    """
    if ring == 0:
        return 1
    else:
        return ring * 8


def cell_count(ring):
    """
    >>> cell_count(0) == contour_len(0)
    True
    >>> cell_count(1) == contour_len(0) + contour_len(1)
    True
    >>> cell_count(2) == contour_len(0) + contour_len(1) + contour_len(2)
    True
    >>> cell_count(2)
    25
    >>> cell_count(3)
    49
    """
    if ring == 0:
        return 1
    else:
        return 1 + 4 * (ring + 1) * ring


def ring_for_cell(cell_no):
    """
    >>> ring_for_cell(0)
    0
    >>> ring_for_cell(3)
    1
    >>> ring_for_cell(9)
    1
    >>> ring_for_cell(10)
    2
    >>> ring_for_cell(46)
    3
    """
    ring = 0
    while cell_count(ring) < cell_no:
        ring = ring + 1
    return ring


def ring_start_cell(ring):
    if ring == 0:
        return 1
    return cell_count(ring - 1) + 1


def ring_origin(ring):
    """
    >>> ring_origin(0)
    [0, 0]
    >>> ring_origin(1)
    [1, 0]
    >>> ring_origin(2)
    [2, -1]
    >>> ring_origin(3)
    [3, -2]
    """
    if ring == 0:
        return [0, 0]
    else:
        return [ring, -(ring - 1)]


def _walk_cells(ring, cell_count):
    coords = ring_origin(ring)
    steps = side_len(ring)

    # Move up. Max: steps -1
    if cell_count <= steps - 1:
        return [coords[0], coords[1] + cell_count]
    else:
        coords[1] += steps - 1
        cell_count -= steps - 1

    # Move left. Max: steps
    if cell_count <= steps:
        return [coords[0] - cell_count, coords[1]]
    else:
        coords[0] -= steps
        cell_count -= steps

    # Move down. Max: steps
    if cell_count <= steps:
        return [coords[0], coords[1] - cell_count]
    else:
        coords[1] -= steps
        cell_count -= steps

    # Move right. Max: steps
    if cell_count <= steps:
        return [coords[0] + cell_count, coords[1]]
    else:
        coords[0] += steps
        cell_count -= steps + 1

    raise IndexError("Moved out of current ring !!!")


def cell_coords(cell_no):
    """
    >>> cell_coords(1)
    [0, 0]
    >>> cell_coords(2)
    [1, 0]
    >>> cell_coords(10)
    [2, -1]
    >>> cell_coords(11)
    [2, 0]
    >>> cell_coords(17)
    [-2, 2]
    """
    # import pdb
    # pdb.set_trace()
    ring = ring_for_cell(cell_no)
    remainder = cell_no - ring_start_cell(ring)
    coords = _walk_cells(ring, remainder)
    return coords


def moves(cell_no):
    return sum(map(abs, cell_coords(cell_no)))


def ring_from_pos(pos):
    return max(pos)


class Step2Grid(object):
    def __init__(self):
        self.pX = 0
        self.pY = 0
        self.grid_size = 50
        self.shift = 25
        self.init_grid()

    def init_grid(self):
        self.grid = [None] * self.grid_size
        for n in range(self.grid_size):
            self.grid[n] = [0] * self.grid_size
        self.grid[self.pX + self.shift][self.pY + self.shift] = 1
        # pprint.pprint(self.grid, indent=1, width=300)

    def values_around(self):
        values = []
        for x in (-1, 0, 1):
            for y in (-1, 0, 1):
                if not (x == 0 and y == 0):
                    val = self.grid[self.pY + y + self.shift][self.pX + x + self.shift]
                    print self.pX, self.pY, '::', x, y, '->', val
                    values.append(val)
        return values

    def something_left(self):
        return self.grid[self.pY + self.shift][self.pX - 1 + self.shift] > 0

    def something_right(self):
        return self.grid[self.pY + self.shift][self.pX + 1 + self.shift] > 0

    def something_above(self):
        return self.grid[self.pY - 1 + self.shift][self.pX + self.shift] > 0

    def something_below(self):
        return self.grid[self.pY + 1 + self.shift][self.pX + self.shift] > 0

    def to_next_pos(self):
        # Special case
        if self.pX == 0 and self.pY == 0:
            self.pX += 1
            print "FIRST: RIGHT"
            return

        if self.something_left() and not self.something_above():
            self.pY -= 1
            print "UP"
            return

        if self.something_below() and not self.something_left():
            self.pX -= 1
            print "LEFT"
            return

        if self.something_right() and not self.something_below():
            self.pY += 1
            print "DOWN"
            return

        if self.something_above() and not self.something_right():
            self.pX += 1
            print "RIGHT"
            return

        raise IndexError

    def walk_until_value(self, value):
        pprint.pprint(self.grid, width=self.grid_size * 4)
        while self.grid[self.pY + self.shift][self.pX + self.shift] < value:
            self.to_next_pos()
            self.grid[self.pY + self.shift][self.pX + self.shift] = sum(self.values_around())
            pprint.pprint(self.grid, width=self.grid_size * 5)
        return self.grid[self.pY + self.shift][self.pX + self.shift]


if __name__ == '__main__':
    gr = Step2Grid()
    value = 265149
    # value = 800
    grid_value = gr.walk_until_value(value)
    print "First cell larger than %d: %d" % (value, grid_value)
