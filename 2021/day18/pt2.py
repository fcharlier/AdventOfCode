#!/usr/bin/python


def read_input(filename):
    """
    >>> read_input('sum1')
    [[[1, 1], [1, 2]], [[2, 3], [2, 4], [1, 5]]]
    >>> read_input('explode1')
    [[[5, 9], [5, 8], [4, 1], [3, 2], [2, 3], [1, 4]]]
    >>> read_input('explode2')
    [[[1, 7], [2, 6], [3, 5], [4, 4], [5, 3], [5, 2]]]
    """
    puzzle = []
    with open(filename) as fdesc:
        for line in fdesc:
            line = line.strip()
            arr = []
            depth = 0
            for char in line:
                if char == "[":
                    depth += 1
                elif char == "]":
                    depth -= 1
                elif char == ",":
                    pass
                else:
                    arr.append([depth, int(char)])
            puzzle.append(arr)
    return puzzle


def explode_where(line):
    return [pos for pos, item in enumerate(line) if item[0] == 5]


def explode(line):
    """
    >>> explode(read_input('explode1')[0])
    [[4, 0], [4, 9], [3, 2], [2, 3], [1, 4]]
    >>> explode(read_input('explode2')[0])
    [[1, 7], [2, 6], [3, 5], [4, 7], [4, 0]]
    >>> explode(read_input('explode3')[0])
    [[2, 6], [3, 5], [4, 7], [4, 0], [1, 3]]
    >>> explode(read_input('explode4')[0])
    [[2, 3], [3, 2], [4, 8], [4, 0], [2, 9], [3, 5], [4, 7], [4, 0]]
    """
    l5_idx = explode_where(line)
    while len(l5_idx) >= 2:
        pos = l5_idx[0]
        if pos > 0:
            line[pos - 1][1] += line[pos][1]
        if pos < len(line) - 2:
            line[pos + 2][1] += line[pos + 1][1]
        line.pop(pos + 1)
        line[pos] = [line[pos][0] - 1, 0]
        l5_idx = explode_where(line)
    return line


def split_where(line):
    return [pos for pos, item in enumerate(line) if item[1] >= 10]


def split(line):
    """
    >>> split([[1, 0], [2, 10], [1, 0]])
    [[1, 0], [3, 5], [3, 5], [1, 0]]
    >>> split([[1, 0], [2, 11], [1, 0]])
    [[1, 0], [3, 5], [3, 6], [1, 0]]
    >>> split([[1, 0], [2, 12], [1, 0]])
    [[1, 0], [3, 6], [3, 6], [1, 0]]
    """
    sp_idx = split_where(line)[0]

    depth, value = line[sp_idx]
    line[sp_idx] = [depth + 1, value // 2]
    line.insert(sp_idx + 1, [depth + 1, (value + 1) // 2])

    return line


def reduce_line(line):
    """
    >>> reduce_line(read_input('reduce1')[0])
    [[4, 0], [4, 7], [3, 4], [4, 7], [4, 8], [4, 6], [4, 0], [2, 8], [2, 1]]
    """

    ew, sw = explode_where(line), split_where(line)
    while len(ew) or len(sw):
        if ew:
            explode(line)
        if sw:
            split(line)
        ew, sw = explode_where(line), split_where(line)

    return line


def add_lines(left, right):
    """
    >>> lines = read_input('reduce2')
    >>> add_lines(lines[0], lines[1])
    [[5, 4], [5, 3], [4, 4], [3, 4], [3, 7], [5, 8], [5, 4], [4, 9], [2, 1], [2, 1]]
    """
    return [[d + 1, v] for d, v in left + right]


def doit(lines):
    """
    >>> doit(read_input('reduce2'))
    [[4, 0], [4, 7], [3, 4], [4, 7], [4, 8], [4, 6], [4, 0], [2, 8], [2, 1]]
    """
    ssum = reduce_line(lines[0])
    for line in lines[1:]:
        ssum = reduce_line(add_lines(ssum, reduce_line(line)))
    return ssum


def magnitude(line):
    """
    >>> magnitude(read_input('mag1')[0])
    143
    >>> magnitude(read_input('mag2')[0])
    1384
    >>> magnitude(read_input('mag3')[0])
    445
    >>> magnitude(read_input('mag4')[0])
    791
    >>> magnitude(read_input('mag5')[0])
    1137
    >>> magnitude(read_input('mag6')[0])
    3488
    """
    maxdepth = max(depth for depth, value in line)
    next_items = [n for n, item in enumerate(line) if item[0] == maxdepth]

    while len(next_items) >= 2 and len(line) > 1:
        l, r = next_items[0:2]
        line[l] = [line[l][0] - 1, line[l][1] * 3 + line[r][1] * 2]
        line.pop(r)
        maxdepth = max(depth for depth, value in line)
        next_items = [n for n, item in enumerate(line) if item[0] == maxdepth]

    return line[0][1]


def part2(lines):
    """
    >>> part2(read_input('example'))
    3993
    """
    results = []
    reduced = []
    for line in lines:
        reduced.append(reduce_line(line))

    for i in range(len(reduced)):
        for j in range(len(reduced)):
            if i != j:
                add1 = add_lines(reduced[i], reduced[j])
                add2 = add_lines(reduced[j], reduced[i])
                red1 = reduce_line(add1)
                red2 = reduce_line(add2)
                results.append(magnitude(red1))
                results.append(magnitude(red2))

    return max(results)


if __name__ == "__main__":
    print(magnitude(doit(read_input("input"))))
    print(part2(read_input("input")))
