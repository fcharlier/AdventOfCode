#!/usr/bin/env python

import itertools

EXAMPLE = """mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)
"""


def parse_recipe(line):
    """Meh
    >>> parse_recipe(EXAMPLE.split("\\n")[0])
    {'ingredients': ['mxmxvkd', 'kfcds', 'sqjhc', 'nhms'], 'allergens': ['dairy', 'fish']}
    """

    line = line.replace(")", "")
    ing, allr = line.split(" (contains")

    return {"ingredients": ing.strip().split(), "allergens": allr.strip().split(", ")}


def parse_recipes(text):
    """
    >>> recipes = parse_recipes(EXAMPLE)
    >>> len(recipes)
    4
    >>> list((len(recipe["ingredients"]) for recipe in recipes))
    [4, 4, 2, 3]
    >>> list((len(recipe["allergens"]) for recipe in recipes))
    [2, 1, 1, 1]
    """
    return [parse_recipe(line) for line in text.strip().split("\n")]


def ingredients_for_allergens(recipes):
    """
    >>> buckets = ingredients_for_allergens(parse_recipes(EXAMPLE))
    >>> sorted(buckets.keys())
    ['dairy', 'fish', 'soy']
    >>> sorted(buckets["soy"])
    ['fvjkl', 'sqjhc']
    >>> sorted(buckets["dairy"])
    ['mxmxvkd']
    """
    all_alrgns = {alrgn: set() for r in recipes for alrgn in r["allergens"]}
    for ingrs, allrgs in ((r["ingredients"], r["allergens"]) for r in recipes):
        for allrg in allrgs:
            if len(all_alrgns[allrg]) == 0:
                all_alrgns[allrg] = set(ingrs)
            else:
                all_alrgns[allrg] &= set(ingrs)
    return all_alrgns


def ingredients_without_allergens(recipes):
    """
    >>> recipes = parse_recipes(EXAMPLE)
    >>> sorted(ingredients_without_allergens(recipes))
    ['kfcds', 'nhms', 'sbzzf', 'trh']
    """
    buckets = ingredients_for_allergens(recipes)
    all_ingrs = [ingr for r in recipes for ingr in r["ingredients"]]
    no_alrgn = set()

    for ingr in set(all_ingrs):
        if not any((ingr in bucket for bucket in buckets.values())):
            no_alrgn.add(ingr)

    return list(no_alrgn)


def count_ingredients_occurrences(recipes, ingredients):
    """
    >>> recipes = parse_recipes(EXAMPLE)
    >>> count_ingredients_occurrences(recipes, ["kfcds"])
    1
    >>> count_ingredients_occurrences(recipes, ["sbzzf"])
    2
    >>> count_ingredients_occurrences(recipes, ["kfcds", "nhms", "sbzzf", "trh"])
    5
    """
    all_ingrs = [ingr for r in recipes for ingr in r["ingredients"]]
    return sum((all_ingrs.count(ingr) for ingr in ingredients))


def reduce_allergens(bkts):
    """
    >>> recipes = parse_recipes(EXAMPLE)
    >>> alrgns = ingredients_for_allergens(recipes)
    >>> reduce_allergens(alrgns)
    {'dairy': {'mxmxvkd'}, 'fish': {'sqjhc'}, 'soy': {'fvjkl'}}
    """
    while not all((len(b) == 1 for b in bkts.values())):
        with_one = [b for b in bkts if len(bkts[b]) == 1]
        for o, b in itertools.product(with_one, bkts):
            if o == b:
                continue
            bkts[b] -= bkts[o]

    return bkts


if __name__ == "__main__":
    with open("input") as fd:
        recipes = parse_recipes(fd.read().strip())
    w_out_alrgns = ingredients_without_allergens(recipes)
    nb_w_out = count_ingredients_occurrences(recipes, w_out_alrgns)
    print(f"Part1: {nb_w_out} ingredients without allergens")
    ingr_for_alrgn = reduce_allergens(ingredients_for_allergens(recipes))
    p2 = ",".join([list(ingr_for_alrgn[k])[0] for k in sorted(ingr_for_alrgn.keys())])
    print(f"Part2: {p2}")
