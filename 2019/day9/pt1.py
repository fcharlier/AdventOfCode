#!/usr/bin/python3


def parse_opcode(opcode):
    code = format(opcode, ">05d")
    # print(code)
    oplen = {
        "01": 4,
        "02": 4,
        "03": 2,
        "04": 2,
        "05": 3,
        "06": 3,
        "07": 4,
        "08": 4,
        "09": 2,
        "99": 1,
    }
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
    >>> process([109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99])
    O: 109 - O: 1 - O: 204 - O: -1 - O: 1001 - O: 100 - O: 1 - O: 100 - O: 1008 - O: 100 - O: 16 - O: 101 - O: 1006 - O: 101 - O: 0 - O: 99 - [109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101, 1006, 101, 0, 99, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 16, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    >>> len(str(process([1102,34915192,34915192,7,4,7,99,0])))
    16
    >>> 104,1125899906842624,99
    ""
    """

    pos = 0
    relbase = 0
    opcode = parse_opcode(intcode[pos])
    while opcode["op"] != 99:
        par1 = par2 = par3 = 0
        if opcode["len"] >= 1:
            if opcode["mode1"] == 0:
                par1 = intcode[pos + 1]
            elif opcode["mode1"] == 1:
                par1 = pos + 1
            elif opcode["mode1"] == 2:
                par1 = intcode[pos + 1] + relbase
        if opcode["len"] >= 2:
            if opcode["mode2"] == 0:
                par2 = intcode[pos + 2]
            elif opcode["mode2"] == 1:
                par2 = pos + 2
            elif opcode["mode2"] == 2:
                par2 = intcode[pos + 2] + relbase
        if opcode["len"] >= 3:
            if opcode["mode3"] == 0:
                par3 = intcode[pos + 3]
            elif opcode["mode3"] == 1:
                par3 = pos + 3
            elif opcode["mode3"] == 2:
                par3 = intcode[pos + 3] + relbase
        jump = False

        if max(par1, par2, par3) > len(intcode) - 1:
            intcode.extend([0] * (max(par1, par2, par3) - len(intcode) + 100))
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
            print("O: %d - " % (intcode[par1]), end="")
        elif opcode["op"] == 5:
            if intcode[par1] != 0:
                pos = intcode[par2]
                jump = True
        elif opcode["op"] == 6:
            if intcode[par1] == 0:
                pos = intcode[par2]
                jump = True
            pass
        elif opcode["op"] == 7:
            if intcode[par1] < intcode[par2]:
                intcode[par3] = 1
            else:
                intcode[par3] = 0
        elif opcode["op"] == 8:
            if intcode[par1] == intcode[par2]:
                intcode[par3] = 1
            else:
                intcode[par3] = 0
        elif opcode["op"] == 9:
            relbase += intcode[par1]

        if not jump:
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
