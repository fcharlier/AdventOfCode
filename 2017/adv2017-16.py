#!/usr/bin/python

# dance = 's1,x3/4,pe/b'
# dancers = ['a', 'b', 'c', 'd', 'e']
dance = open('adv2017-16.input').read().strip()
dancers = list('abcdefghijklmnop')


def spin(dancers, count):
    while count:
        dancer = dancers.pop()
        dancers.insert(0, dancer)
        count = count - 1


def exchange(dancers, posA, posB):
    """dancers at posA and posB switch places"""
    dancers[posA], dancers[posB] = dancers[posB], dancers[posA]


def partner(dancers, nameA, nameB):
    """dancers named A and B switch places"""
    posA = dancers.index(nameA)
    posB = dancers.index(nameB)
    exchange(dancers, posA, posB)


def do_dance(dance, dancers):
    moves = dance.split(',')
    # print ''.join(dancers)
    for move in moves:
        if move[0] == 's':
            spin(dancers, int(move[1:]))
        if move[0] == 'x':
            poss = map(int, move[1:].split('/'))
            exchange(dancers, *poss)
        if move[0] == 'p':
            poss = move[1:].split('/')
            partner(dancers, *poss)
        # print ''.join(dancers)


if __name__ == '__main__':
    dancers_zero = ''.join(dancers)
    reps = 1000000000
    steps_to_zero = None
    for n in xrange(reps):
        do_dance(dance, dancers)
        if steps_to_zero is not None:
            steps_to_zero -= 1
            if steps_to_zero == 0:
                break
        if ''.join(dancers) == dancers_zero:
            steps_to_zero = reps % (n + 1)
            print 'At %d dances, reached initial state' % (n + 1)
            print reps % (n + 1)
    print ''.join(dancers)
