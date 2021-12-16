#!/usr/bin/env python


def read_input(filename):
    """
    >>> read_input('ex1')
    'D2FE28'
    """
    with open(filename) as fd:
        return fd.readline().strip()


def h2b(pkts):
    """
    >>> h2b(read_input('ex1'))
    '110100101111111000101000'
    """
    return "".join(f"{int(c, 16):>04b}" for c in pkts)


def pkt_ver(pkt):
    """
    >>> pkt_ver(h2b(read_input('ex1')))
    6
    >>> pkt_ver(h2b(read_input('ex2')))
    1
    >>> pkt_ver(h2b(read_input('ex3')))
    7
    """
    return int(pkt[:3], 2)


def pkt_type(pkt):
    """
    >>> pkt_type(h2b(read_input('ex1')))
    4
    >>> pkt_type(h2b(read_input('ex2')))
    6
    >>> pkt_type(h2b(read_input('ex3')))
    3
    """
    return int(pkt[3:6], 2)


def literal_value(pkt):
    """
    >>> literal_value(h2b(read_input('ex1')))
    (2021, 21)
    >>> literal_value('11010001010')
    (10, 11)
    """
    loc = 6
    binstr = ""
    while pkt[loc] == "1":
        binstr += pkt[loc + 1 : loc + 5]
        loc += 5
    return int(binstr + pkt[loc + 1 : loc + 5], 2), loc + 5


def pkt_sumver(pkt):  # returns (versions:list, size:int)
    """
    >>> pkt_sumver(h2b(read_input('ex1')))
    (6, 21)
    >>> pkt_sumver(h2b(read_input('ex2')))
    (9, 49)
    >>> pkt_sumver(h2b(read_input('ex3')))
    (14, 51)
    >>> pkt_sumver(h2b('8A004A801A8002F478'))[0]
    16
    >>> pkt_sumver(h2b('620080001611562C8802118E34'))[0]
    12
    >>> pkt_sumver(h2b('C0015000016115A2E0802F182340'))[0]
    23
    >>> pkt_sumver(h2b('A0016C880162017C3686B18A3D4780'))[0]
    31
    """
    ver = pkt_ver(pkt)

    if pkt_type(pkt) == 4:
        _, size = literal_value(pkt)
        return ver, size
    else:  # All other packet types
        if pkt[6] == "0":
            sub_len = int(pkt[7:22], 2)
            sub = pkt[22 : 22 + sub_len]
            pos = 0
            while pos < sub_len:
                vsub, ssub = pkt_sumver(sub[pos:])
                ver += vsub
                pos += ssub
            return ver, 22 + pos
        elif pkt[6] == "1":
            n_sub = int(pkt[7:18], 2)
            pos = 18
            for _ in range(n_sub):
                vsub, ssub = pkt_sumver(pkt[pos:])
                ver += vsub
                pos += ssub
            return ver, pos


def main(filename):
    return pkt_sumver(h2b(read_input(filename)))[0]



if __name__ == "__main__":
    print(main('input'))
