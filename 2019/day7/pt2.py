#!/usr/bin/python3

from itertools import permutations


def parse_opcode(opcode):
    code = format(opcode, ">05d")
    oplen = {"01": 4, "02": 4, "03": 2, "04": 2, "05": 3, "06": 3, "07": 4, "08": 4, "99": 1}
    return {
        "op": int(code[3:5]),
        "len": oplen[code[3:5]],
        "mode1": int(code[2]),
        "mode2": int(code[1]),
        "mode3": int(code[0]),
    }


def process(intcode, in_setting, in_signal, start_pos):
    pos = start_pos
    opcode = parse_opcode(intcode[pos])

    if start_pos != 0:
        inputs = [in_signal, None]
    else:
        inputs = [in_setting, in_signal]

    while opcode["op"] != 99:
        if opcode["len"] >= 1:
            par1 = pos + 1 if opcode["mode1"] else intcode[pos + 1]
        if opcode["len"] >= 2:
            par2 = pos + 2 if opcode["mode2"] else intcode[pos + 2]
        if opcode["len"] >= 3:
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
            return intcode[par1], pos + opcode["len"]
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

    # print("Nothing to do anymore")
    return None, None


def run_amp_circuit(intcode, phase_signal):
    """Run phase signal in the intcode

    >>> run_amp_circuit([3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5], (9, 8, 7, 6, 5))
    139629729
    >>> run_amp_circuit([3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10], (9, 7, 8, 5, 6))
    18216
    """
    signal = 0

    amps = {
        "A": intcode.copy(),
        "B": intcode.copy(),
        "C": intcode.copy(),
        "D": intcode.copy(),
        "E": intcode.copy(),
    }
    pos = dict(zip(amps.keys(), [0, 0, 0, 0, 0]))
    phase_signal = dict(zip(amps.keys(), phase_signal))

    signal = 0
    result_E = None
    while signal is not None:
        for amp in pos.keys():
            # print("Running %s ..." % amp)
            signal, pos[amp] = process(amps[amp], phase_signal[amp], signal, pos[amp])
            # print("Done running %s. Returned %d" % (amp, signal))
            if amp == "E" and signal is not None:
                result_E = signal
#
    return result_E


def read_input():
    with open("data") as data:
        data = data.read().split(",")
        intcode = list(map(int, data))
    return intcode


if __name__ == "__main__":
    intcode = read_input()

    maxim = 0
    for signal in permutations([5, 6, 7, 8, 9]):
        result = run_amp_circuit(intcode, signal)
        print("Signal: %s   => %d" % (signal, result))
        maxim = max(result, maxim)
    print("Maximal signal: %d" % maxim)
