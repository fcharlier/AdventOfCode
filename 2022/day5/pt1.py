#!/usr/bin/python3

""" 2022 day 5 part 1
"""


def parse_input(filename):
    """Parses an input into useful data structures
    >>> c, s = parse_input("input_example")
    >>> c == [['Z', 'N'], ['M', 'C', 'D'], ['P']]
    True
    >>> s == [{'count': 1, 'src': 2, 'dst': 1}, {'count': 3, 'src': 1, 'dst': 3}, {'count': 2, 'src': 2, 'dst': 1}, {'count': 1, 'src': 1, 'dst': 2}, ]
    True
    """

    cratelines = []
    numbers = None
    steps = []
    with open(filename) as fd:
        for line in fd.readlines():
            if "[" in line:
                cratelines.append(line)
            elif line.startswith("move"):
                step = line.strip().split(" ")
                steps.append(
                    {"count": int(step[1]), "src": int(step[3]), "dst": int(step[5])}
                )
            elif "1" in line:
                numbers = list(map(int, (n for n in line.strip().split(" ") if n)))
    crates = [[] for n in numbers]
    for n in numbers:
        for crateline in cratelines:
            loc = (n - 1) * 4 + 1
            if (content := crateline[loc]).isupper():
                crates[n - 1].append(content)

    for n in range(len(crates)):
        crates[n].reverse()
    return crates, steps


def do_step(crates, step):
    """Runs a step
    >>> c, s = parse_input("input_example")
    >>> do_step(c, s[0])
    >>> c[0] == ['Z', 'N', 'D']
    True
    >>> c[1] == ['M', 'C']
    True
    >>> c[2] == ['P']
    True
    >>> do_step(c, s[1])
    >>> c[0] == []
    True
    >>> c[1] == ['M', 'C']
    True
    >>> c[2] == ['P', 'D', 'N', 'Z']
    True
    """
    cnt, src, dst = step.values()
    crates[dst - 1].extend(crates[src - 1][-cnt:][::-1])
    crates[src - 1] = crates[src - 1][:-cnt]


def main(filename):
    """Do it all
    >>> main("input_example")
    CMZ
    """
    crates, steps = parse_input(filename)
    for step in steps:
        do_step(crates, step)
    message = "".join(crate[-1] for crate in crates)
    print(message)


if __name__ == "__main__":
    main("input_real")
