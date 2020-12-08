#!/usr/bin/env python3

import pprint


def read_ingredient(ingstr):
    ingstr = ingstr.strip()
    ing = ingstr.split(" ")
    return {"qty": int(ing[0]), "name": ing[1]}


def read_reaction(line):
    raw_inputs, raw_output = line.split(" => ")

    output = read_ingredient(raw_output)

    raw_inputs = raw_inputs.split(", ")
    inputs = {}
    for ingstr in raw_inputs:
        ingr = read_ingredient(ingstr)
        inputs[ingr["name"]] = ingr["qty"]

    return output, inputs


def read_reactions(filename):
    reactions = {}
    with open(filename) as data:
        for line in data.readlines():
            line.strip()
            if len(line):
                output, inputs = read_reaction(line)
                reactions[output["name"]] = {"quantity": output["qty"], "inputs": inputs}
    return reactions


def update_required(required, elements):
    for element in elements:
        if element["name"] not in required:
            required[element["name"]] = 0
        required[element["name"]] += element["qty"]


def requires_only_ore(reactions):
    result = set()
    for reac in reactions:
        if len(reactions[reac]["inputs"]) == 1 and "ORE" in reactions[reac]["inputs"]:
            result.add(reac)


if __name__ == "__main__":
    reactions = read_reactions("data0")
    pprint.pprint(reactions)
    print(cant_be_produced(reactions))
