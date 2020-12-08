#!/usr/bin/env python

from itertools import combinations
import re


class Planet(object):
    vx = 0
    vy = 0
    vz = 0

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return "%d(%+d) | %d(%+d) | %d(%+d)" % (self.x, self.vx, self.y, self.vy, self.z, self.vz)

    @property
    def potential_energy(self):
        return abs(self.x) + abs(self.y) + abs(self.z)

    @property
    def kinetic_energy(self):
        return abs(self.vx) + abs(self.vy) + abs(self.vz)

    @property
    def total_energy(self):
        return self.potential_energy * self.kinetic_energy

    def apply_velocity_x(self):
        self.x += self.vx

    def apply_velocity_y(self):
        self.y += self.vy

    def apply_velocity_z(self):
        self.z += self.vz

    def apply_gravity_x(self, other):
        if self.x > other.x:
            self.vx -= 1
            other.vx += 1
        elif self.x < other.x:
            self.vx += 1
            other.vx -= 1

    def apply_gravity_y(self, other):
        if self.y > other.y:
            self.vy -= 1
            other.vy += 1
        elif self.y < other.y:
            self.vy += 1
            other.vy -= 1

    def apply_gravity_z(self, other):
        if self.z > other.z:
            self.vz -= 1
            other.vz += 1
        elif self.z < other.z:
            self.vz += 1
            other.vz -= 1


def parse_data(data):
    planets = []

    for line in data.split("\n"):
        if len(line):
            m = re.match(r"<x=(?P<x>-?\d+),\s+y=(?P<y>-?\d+),\s+z=(?P<z>-?\d+)>", line)
            planets.append(Planet(int(m.group("x")), int(m.group("y")), int(m.group("z"))))

    return planets


def apply_gravity_x(planets):
    for pair in combinations(planets, 2):
        pair[0].apply_gravity_x(pair[1])


def apply_gravity_y(planets):
    for pair in combinations(planets, 2):
        pair[0].apply_gravity_y(pair[1])


def apply_gravity_z(planets):
    for pair in combinations(planets, 2):
        pair[0].apply_gravity_z(pair[1])


def apply_velocity_x(planets):
    for planet in planets:
        planet.apply_velocity_x()


def apply_velocity_y(planets):
    for planet in planets:
        planet.apply_velocity_y()


def apply_velocity_z(planets):
    for planet in planets:
        planet.apply_velocity_z()


def iteration_x(planets):
    apply_gravity_x(planets)
    apply_velocity_x(planets)


def iteration_y(planets):
    apply_gravity_y(planets)
    apply_velocity_y(planets)


def iteration_z(planets):
    apply_gravity_z(planets)
    apply_velocity_z(planets)


def energy(planets):
    return sum((planet.total_energy for planet in planets))


if __name__ == "__main__":
    data = """<x=13, y=9, z=5>
<x=8, y=14, z=-2>
<x=-5, y=4, z=11>
<x=2, y=-6, z=1>
"""
    planets = parse_data(data)
    history = str(planets)
    step = 0
    while step == 0 or str(planets) != history:
        iteration_z(planets)
        step += 1
        if step % 1000 == 0:
            print(step)
    print(step)


# In [1]: x=268296
#
# In [2]: y=161428
#
# In [3]: z=102356
#
# In [4]: x/z
# Out[4]: 2.621204423775841
#
# In [5]: y/z
# Out[5]: 1.5771229825315565
#
# In [6]: x/y
# Out[6]: 1.662016502713284
#
# In [7]: 4*z
# Out[7]: 409424
#
# In [8]: import math
#
# In [9]: math.gcd(x,y)
# Out[9]: 4
#
# In [10]: x*y/4
# Out[10]: 10827621672.0
#
# In [11]: xy=x*y//4
#
# In [12]: xy
# Out[12]: 10827621672
#
# In [13]: math.gcd(xy,z)
# Out[13]: 4
#
# In [14]: xy*z//4
# Out[14]: 277068010964808
