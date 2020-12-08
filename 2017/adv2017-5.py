#!/usr/bin/python


def load_jumplist(jl):
    with open(jl) as lines:
        return map(int, [line.strip() for line in lines])


def process_jumps(jumplist):
    cur = 0
    steps = 0
    while cur >= 0 and cur < len(jumplist):
        _next = cur + jumplist[cur]
        jumplist[cur] += 1
        cur = _next
        steps += 1
    return steps


def process_jumps_complex(jumplist):
    cur = 0
    steps = 0
    while cur >= 0 and cur < len(jumplist):
        _next = cur + jumplist[cur]
        if jumplist[cur] >= 3:
            jumplist[cur] -= 1
        else:
            jumplist[cur] += 1
        cur = _next
        steps += 1
    return steps


if __name__ == '__main__':
    jumplist = [0, 3, 0, 1, -3]
    jumplist = load_jumplist('adv2017-5.input')
    print process_jumps(jumplist)

    jumplist = [0, 3, 0, 1, -3]
    jumplist = load_jumplist('adv2017-5.input')
    print process_jumps_complex(jumplist)
