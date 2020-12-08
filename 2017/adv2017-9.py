#!/usr/bin/python

"""
<>, empty garbage.
<random characters>, garbage containing random characters.
<<<<>, because the extra < are ignored.
<{!>}>, because the first > is canceled.
<!!>, because the second ! is canceled, allowing the > to terminate the garbage.
<!!!>>, because the second ! and the first > are canceled.
<{o"i!a,<{i<a>, which ends at the first >.

{}, 1 group.
{{{}}}, 3 groups.
{{},{}}, also 3 groups.
{{{},{},{{}}}}, 6 groups.
{<{},{},{{}}>}, 1 group (which itself contains garbage).
{<a>,<a>,<a>,<a>}, 1 group.
{{<a>},{<a>},{<a>},{<a>}}, 5 groups.
{{<!>},{<!>},{<!>},{<a>}}, 2 groups (since all but the last > are canceled).


{}, score of 1.
{{{}}}, score of 1 + 2 + 3 = 6.
{{},{}}, score of 1 + 2 + 2 = 5.
{{{},{},{{}}}}, score of 1 + 2 + 3 + 3 + 3 + 4 = 16.
{<a>,<a>,<a>,<a>}, score of 1.
{{<ab>},{<ab>},{<ab>},{<ab>}}, score of 1 + 2 + 2 + 2 + 2 = 9.
{{<!!>},{<!!>},{<!!>},{<!!>}}, score of 1 + 2 + 2 + 2 + 2 = 9.
{{<a!>},{<a!>},{<a!>},{<ab>}}, score of 1 + 2 = 3.
"""


def groups_score(str_group):
    """
    >>> groups_score('<>')
    {'score': 0, 'groups': 0, 'garbage': 0}

    >>> groups_score('<<<<>')
    {'score': 0, 'groups': 0, 'garbage: 3}

    >>> groups_score('<{!>}>')
    {'score': 0, 'groups': 0, 'garbage': 2}

    >>> groups_score('<!!>')
    {'score': 0, 'groups': 0, 'garbage': 0}

    >>> groups_score('<!!!>>')
    {'score': 0, 'groups': 0, 'garbage': 0}

    >>> groups_score('<{o"i!a,<{i<a>')
    {'score': 0, 'groups': 0, 'garbage': 10}

    >>> groups_score('{}')
    {'score': 1, 'groups': 1, 'garbage': 0}

    >>> groups_score('{{{}}}')
    {'score': 6, 'groups': 3, 'garbage': 0}

    >>> groups_score('{{},{}}')
    {'score': 5, 'groups': 3, 'garbage': 0}

    >>> groups_score('{{{},{},{{}}}}')
    {'score': 16, 'groups': 6, 'garbage': 0}

    >>> groups_score('{<a>,<a>,<a>,<a>}')
    {'score': 1, 'groups': 1, 'garbage': 4}

    >>> groups_score('{{<a>},{<a>},{<a>},{<a>}}')
    {'score': 9, 'groups': 5, 'garbage': 4}

    >>> groups_score('{{<a!>},{<a!>},{<a!>},{<ab>}}')
    {'score': 3, 'groups': 2, 'garbage': 17}

    """
    in_garbage = False
    current_level = 0
    groups = 0
    score = 0
    garbage = 0
    n = 0

    while n < len(str_group):
        if str_group[n] == '!':
            n += 2
            continue

        if str_group[n] == '>':
            in_garbage = False
            n += 1
            continue

        if in_garbage:
            n += 1
            garbage += 1
            continue

        if str_group[n] == '<':
            in_garbage = True
            n += 1
            continue

        if str_group[n] == '{':
            groups += 1
            current_level += 1
            score += current_level
            n += 1
            continue

        if str_group[n] == '}':
            current_level -= 1
            n += 1
            continue

        n += 1

    return {'score': score, 'garbage': garbage, 'groups': groups}


if __name__ == '__main__':
    with open('adv2017-9.input') as puzzle_fd:
        print groups_score(puzzle_fd.read())
