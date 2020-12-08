#!/usr/bin/python3


def fuel(mass):
    return mass // 3 - 2


with open("data") as data:
    lines = data.readlines()
masses = map(int, lines)
fuel = map(fuel, masses)
print(sum(fuel))
