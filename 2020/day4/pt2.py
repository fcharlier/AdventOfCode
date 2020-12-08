#!/usr/bin/env python

import re


def parse_passport(passport_text):
    cut = passport_text.strip().split()
    tuples = (el.split(":") for el in cut)
    return dict(tuples)


def check_passport(passport_dict):
    """Meh
    >>> check_passport(parse_passport("eyr:1972 cid:100 hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926"))
    False
    >>> check_passport(parse_passport("iyr:2019 hcl:#602927 eyr:1967 hgt:170cm ecl:grn pid:012533040 byr:1946"))
    False
    >>> check_passport(parse_passport("hcl:dab227 iyr:2012 ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277"))
    False
    >>> check_passport(parse_passport("hgt:59cm ecl:zzz eyr:2038 hcl:74454a iyr:2023 pid:3556412378 byr:2007"))
    False
    >>> check_passport(parse_passport("pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980 hcl:#623a2f"))
    True
    >>> check_passport(parse_passport("eyr:2029 ecl:blu cid:129 byr:1989 iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm"))
    True
    >>> check_passport(parse_passport("hcl:#888785 hgt:164cm byr:2001 iyr:2015 cid:88 pid:545766238 ecl:hzl eyr:2022"))
    True
    >>> check_passport(parse_passport("iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719"))
    True
    >>> check_passport(parse_passport("iyr:2010 hgt:158dm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719"))
    False
    >>> check_passport(parse_passport("iyr:2010 hgt:158cm hcl:#b6652a ecl:ora byr:1944 eyr:2021 pid:093154719"))
    False
    >>> check_passport(parse_passport("iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1919 eyr:2021 pid:093154719"))
    False
    >>> check_passport(parse_passport("iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1920 eyr:2021 pid:093154719"))
    True
    >>> check_passport(parse_passport("iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1920 eyr:2021 pid:a93154719"))
    False
    >>> check_passport(parse_passport("iyr:2009 hgt:158cm hcl:#b6652a ecl:blu byr:1920 eyr:2021 pid:093154719"))
    False
    >>> check_passport(parse_passport("iyr:2021 hgt:158cm hcl:#b6652a ecl:blu byr:1920 eyr:2021 pid:093154719"))
    False
    >>> check_passport(parse_passport("iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1920 eyr:2021 pid:093154719"))
    True
    """
    required_keys = {"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"}
    if not set(passport_dict.keys()).issuperset(required_keys):
        return False


    if not 1920 <= int(passport_dict["byr"]) <= 2002:
        return False

    if not 2010 <= int(passport_dict["iyr"]) <= 2020:
        return False

    if not 2020 <= int(passport_dict["eyr"]) <= 2030:
        return False

    hgt = re.fullmatch(r"(\d+)(cm|in)", passport_dict["hgt"])
    if not hgt:
        return False
    h = hgt.group(1)
    u = hgt.group(2)
    if u == "cm":
        if not 150 <= int(h) <= 193:
            return False
    if u == "in":
        if not 59 <= int(h) <= 76:
            return False

    hcl = re.fullmatch(r"^\#[a-z0-9]{6}$", passport_dict["hcl"])
    if not hcl:
        return False

    if not passport_dict["ecl"] in {"amb", "blu", "brn", "gry", "grn", "hzl", "oth"}:
        return False

    if not re.fullmatch(r"^\d{9}$", passport_dict["pid"]):
        return False

    return True


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

    # zippd = zip(passports, checked)
    # import pprint
    # pprint.pprint([p for p in zippd if p[1]])
    #
