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


def op_sum(vals):
    return sum(vals)


def op_prod(vals):
    p = 1
    for v in vals:
        p *= v
    return p


def op_gt(vals):
    return int(vals[0] > vals[1])


def op_lt(vals):
    return int(vals[0] < vals[1])


def op_eq(vals):
    return int(vals[0] == vals[1])


def pkt_sumver(pkt):
    """
    >>> pkt_sumver(h2b('C200B40A82'))[2]
    3
    >>> pkt_sumver(h2b('04005AC33890'))[2]
    54
    >>> pkt_sumver(h2b('880086C3E88112'))[2]
    7
    >>> pkt_sumver(h2b('CE00C43D881120'))[2]
    9
    >>> pkt_sumver(h2b('D8005AC2A8F0'))[2]
    1
    >>> pkt_sumver(h2b('F600BC2D8F'))[2]
    0
    >>> pkt_sumver(h2b('9C005AC2F8F'))[2]
    0
    >>> pkt_sumver(h2b('9C0141080250320F1802104A08'))[2]
    1
    """
    ver = pkt_ver(pkt)
    ptype = pkt_type(pkt)

    op = {
        0: op_sum,
        1: op_prod,
        2: min,
        3: max,
        5: op_gt,
        6: op_lt,
        7: op_eq,
    }

    if ptype == 4:
        val, size = literal_value(pkt)
        return ver, size, val
    else:  # All other packet types
        vals = []
        if pkt[6] == "0":
            sub_len = int(pkt[7:22], 2)
            sub = pkt[22 : 22 + sub_len]
            pos = 0
            while pos < sub_len:
                vsub, ssub, val = pkt_sumver(sub[pos:])
                ver += vsub
                pos += ssub
                vals.append(val)

            return ver, 22 + pos, op[ptype](vals)

        elif pkt[6] == "1":
            n_sub = int(pkt[7:18], 2)
            pos = 18
            for _ in range(n_sub):
                vsub, ssub, val = pkt_sumver(pkt[pos:])
                ver += vsub
                pos += ssub
                vals.append(val)

            return ver, pos, op[ptype](vals)


def main(filename):
    return pkt_sumver(h2b(read_input(filename)))[2]


if __name__ == "__main__":
    print(main("input"))
