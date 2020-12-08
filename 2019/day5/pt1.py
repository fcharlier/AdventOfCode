#!/usr/bin/python3


def parse_opcode(opcode):
    code = format(opcode, ">05d")
    # print(code)
    oplen = {"01": 4, "02": 4, "03": 2, "04": 2, "99": 1}
    return {
        "op": int(code[3:5]),
        "len": oplen[code[3:5]],
        "mode1": int(code[2]),
        "mode2": int(code[1]),
        "mode3": int(code[0]),
    }


def process(intcode):
    """Processes an intcode

    >>> process([1,9,10,3,99,3,11,0,99,30,40,50])
    [1, 9, 10, 70, 99, 3, 11, 0, 99, 30, 40, 50]
    >>> process([1, 0, 0, 0, 99])
    [2, 0, 0, 0, 99]
    >>> process([2, 3, 0, 3, 99])
    [2, 3, 0, 6, 99]
    >>> process([2, 4, 4, 5, 99, 0])
    [2, 4, 4, 5, 99, 9801]
    >>> process([1, 1, 1, 4, 99, 5, 6, 0, 99])
    [30, 1, 1, 4, 2, 5, 6, 0, 99]
    """

    pos = 0
    opcode = parse_opcode(intcode[pos])
    while opcode["op"] != 99:
        if opcode["len"] >= 1:
            par1 = pos + 1 if opcode["mode1"] else intcode[pos + 1]
        if opcode["len"] >= 2:
            par2 = pos + 2 if opcode["mode2"] else intcode[pos + 2]
        if opcode["len"] >= 2:
            par3 = intcode[pos + 3]

        if opcode["op"] == 1:
            # print(">>> %d + %d. Store in cell#%d" % (intcode[par1], intcode[par2], par3))
            intcode[par3] = intcode[par1] + intcode[par2]
        elif opcode["op"] == 2:
            # print(">>> %d * %d. Store in cell#%d" % (intcode[par1], intcode[par2], par3))
            intcode[par3] = intcode[par1] * intcode[par2]
        elif opcode["op"] == 3:
            # print(">>> Input. Store in %d" % (par1))
            intcode[par1] = int(input("Input: "))
        elif opcode["op"] == 4:
            # print(">>> Output. Get cell#%d" % (par1))
            print("Output: %d" % intcode[par1])
        pos += opcode["len"]
        # print("Pos: %d - Opcode: %s" % (pos, intcode[pos]))
        opcode = parse_opcode(intcode[pos])

    return intcode


def read_input():
    with open("data") as data:
        data = data.read().split(",")
        intcode = list(map(int, data))
    return intcode


if __name__ == "__main__":
    intcode = read_input()
    process(intcode)
