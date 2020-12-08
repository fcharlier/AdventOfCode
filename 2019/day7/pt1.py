#!/usr/bin/python3

from itertools import permutations


def parse_opcode(opcode):
    code = format(opcode, ">05d")
    # print(code)
    oplen = {"01": 4, "02": 4, "03": 2, "04": 2, "05": 3, "06": 3, "07": 4, "08": 4, "99": 1}
    return {
        "op": int(code[3:5]),
        "len": oplen[code[3:5]],
        "mode1": int(code[2]),
        "mode2": int(code[1]),
        "mode3": int(code[0]),
    }


def process(intcode, phase_setting, signal_in):
    """Processes an intcode

    >>> process([1,9,10,3,99,3,11,0,99,30,40,50], 0, 0)
    [1, 9, 10, 70, 99, 3, 11, 0, 99, 30, 40, 50]
    >>> process([1, 0, 0, 0, 99], 0, 0)
    [2, 0, 0, 0, 99]
    >>> process([2, 3, 0, 3, 99], 0, 0)
    [2, 3, 0, 6, 99]
    >>> process([2, 4, 4, 5, 99, 0], 0, 0)
    [2, 4, 4, 5, 99, 9801]
    >>> process([1, 1, 1, 4, 99, 5, 6, 0, 99], 0, 0)
    [30, 1, 1, 4, 2, 5, 6, 0, 99]
    """

    inputs = [phase_setting, signal_in]

    pos = 0
    opcode = parse_opcode(intcode[pos])
    while opcode["op"] != 99:
        if opcode["len"] >= 1:
            par1 = pos + 1 if opcode["mode1"] else intcode[pos + 1]
        if opcode["len"] >= 2:
            par2 = pos + 2 if opcode["mode2"] else intcode[pos + 2]
        if opcode["len"] >= 2:
            par3 = intcode[pos + 3]
        jump = False

        if opcode["op"] == 1:
            # print(">>> %d + %d. Store in cell#%d" % (intcode[par1], intcode[par2], par3))
            intcode[par3] = intcode[par1] + intcode[par2]
        elif opcode["op"] == 2:
            # print(">>> %d * %d. Store in cell#%d" % (intcode[par1], intcode[par2], par3))
            intcode[par3] = intcode[par1] * intcode[par2]
        elif opcode["op"] == 3:
            # print(">>> Input. Store in %d" % (par1))
            intcode[par1] = inputs.pop(0)
        elif opcode["op"] == 4:
            # print(">>> Output. Get cell#%d" % (par1))
            return intcode[par1]
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

        if not jump:
            pos += opcode["len"]
        # print("Pos: %d - Opcode: %s" % (pos, intcode[pos]))
        opcode = parse_opcode(intcode[pos])

    return intcode


def run_amp_circuit(intcode, phase_signal):
    """Run phase signal in the intcode

    >>> run_amp_circuit([3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0], (4, 3, 2, 1, 0))
    43210
    >>> run_amp_circuit([3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0], (0, 1, 2, 3, 4))
    54321
    >>> run_amp_circuit([3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0], (1, 0, 4, 3, 2))
    65210
    """
    signal = 0
    for setting in phase_signal:
        signal = process(intcode.copy(), setting, signal)
    return signal


def read_input():
    with open("data") as data:
        data = data.read().split(",")
        intcode = list(map(int, data))
    return intcode


if __name__ == "__main__":
    intcode = read_input()

    maxim = 0
    for signal in permutations([0, 1, 2, 3, 4]):
        result = run_amp_circuit(intcode, signal)
        print("Signal: %s   => %d" % (signal, result))
        maxim = max(result, maxim)
    print("Maximal signal: %d" % maxim)
