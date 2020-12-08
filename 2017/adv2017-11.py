#!/usr/bin/python

def simplify(moves):
    count_before = sum(moves.values())
    count_after = count_before + 1
    while count_before != count_after:
        count_before = count_after
        ne_sw = min(moves['ne'], moves['sw'])
        moves['ne'] -= ne_sw
        moves['sw'] -= ne_sw

        nw_se = min(moves['nw'], moves['se'])
        moves['nw'] -= nw_se
        moves['se'] -= nw_se

        n_s = min(moves['n'], moves['s'])
        moves['n'] -= n_s
        moves['s'] -= n_s

        ne_s = min(moves['ne'], moves['s'])
        moves['ne'] -= ne_s
        moves['s'] -= ne_s
        moves['se'] += ne_s

        se_n = min(moves['se'], moves['n'])
        moves['se'] -= se_n
        moves['n'] -= se_n
        moves['ne'] += se_n

        nw_s = min(moves['nw'], moves['s'])
        moves['nw'] -= nw_s
        moves['s'] -= nw_s
        moves['sw'] += nw_s

        sw_n = min(moves['sw'], moves['n'])
        moves['sw'] -= sw_n
        moves['n'] -= sw_n
        moves['ne'] += sw_n

        ne_nw = min(moves['ne'], moves['nw'])
        moves['nw'] -= ne_nw
        moves['ne'] -= ne_nw
        moves['n'] += ne_nw

        se_sw = min(moves['se'], moves['sw'])
        moves['sw'] -= se_sw
        moves['se'] -= se_sw
        moves['s'] += se_sw

        count_after = sum(moves.values())
        print "Reduced to %d moves." % count_after

    return moves


def move(path):
    """
    >>> move('ne,ne,ne')
    3

    >>> move('ne,ne,sw,sw')
    0

    >>> move('ne,ne,s,s')
    2

    >>> move('se,sw,se,sw,se,sw')
    3

    """
    moves = {
        'ne': 0,
        'se': 0,
        'nw': 0,
        'sw': 0,
        'n': 0,
        's': 0,
    }

    path = path.split(',')
    furthest = 0
    for step in path:
        moves[step] += 1
        furthest = max(furthest, sum(simplify(moves.copy()).values()))

    moves = simplify(moves)

    print moves
    print furthest
    return sum(moves.values())


if __name__ == '__main__':
    with open('adv2017-11.input') as path_fd:
        print move(path_fd.read().strip())
