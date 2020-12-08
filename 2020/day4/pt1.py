#!/usr/bin/env python


def parse_passport(passport_text):
    cut = passport_text.strip().split()
    tuples = (el.split(":") for el in cut)
    return dict(tuples)


def check_passport(passport_dict):
    """Meh
    >>> check_passport({"ecl": "gry", "pid":"860033327", "eyr":"2020", "hcl":"#fffffd",\
    "byr":"1937", "iyr":"2017", "cid":"147", "hgt":"183cm"})
    True
    >>> check_passport({"iyr":"2013", "ecl":"amb", "cid":"350", "eyr":"2023",\
    "pid":"028048884", "hcl":"#cfa07d", "byr":"1929"})
    False
    >>> check_passport({"hcl":"#ae17e1", "iyr":"2013", "eyr":"2024", "ecl":"brn",\
    "pid":"760753108", "byr":"1931", "hgt":"179cm" })
    True
    >>> check_passport({"hcl":"#cfa07d", "eyr":"2025", "pid":"166559648", "iyr":"2011",\
    "ecl":"brn", "hgt":"59in"})
    False
    """
    required_keys = {"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"}
    return set(passport_dict.keys()).issuperset(required_keys)


if __name__ == "__main__":
    with open("input") as fd:
        data = fd.read()
    passports = data.split("\n\n")
    for passport in passports:
        if len(passport) < 4:
            raise
    passports = list((parse_passport(text) for text in passports))
    checked = list((check_passport(passport) for passport in passports))

    print("Invalid: ", checked.count(False))
    print("Valid: ", checked.count(True))
