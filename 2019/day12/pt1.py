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

    def apply_velocity(self):
        self.x += self.vx
        self.y += self.vy
        self.z += self.vz

    def apply_gravity(self, other):
        if self.x > other.x:
            self.vx -= 1
            other.vx += 1
        elif self.x < other.x:
            self.vx += 1
            other.vx -= 1

        if self.y > other.y:
            self.vy -= 1
            other.vy += 1
        elif self.y < other.y:
            self.vy += 1
            other.vy -= 1

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


def apply_gravity(planets):
    for pair in combinations(planets, 2):
        pair[0].apply_gravity(pair[1])


def apply_velocity(planets):
    for planet in planets:
        planet.apply_velocity()


def iteration(planets):
    apply_gravity(planets)
    apply_velocity(planets)


def energy(planets):
    return sum((planet.total_energy for planet in planets))


if __name__ == "__main__":
    data = """<x=13, y=9, z=5>
<x=8, y=14, z=-2>
<x=-5, y=4, z=11>
<x=2, y=-6, z=1>
"""
    planets = parse_data(data)
    for n in range(1000):
        iteration(planets)
    print(energy(planets))
