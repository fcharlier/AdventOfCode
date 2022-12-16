#!/usr/bin/python3

import re


def read_input(filename):
    """
    >>> valves = read_input("input_example")
    >>> valves   # doctest: +ELLIPSIS
    {'AA':...'II',)}}
    >>> len(valves)
    10
    """
    valves = {}
    valve_re = re.compile(
        r"Valve ([A-Z]{2}) has flow rate=(\d+); tunnels? leads? to valves? ([A-Z, ]+)"
    )
    with open(filename) as fd:
        for line in fd:
            if m := valve_re.search(line):
                valves[m.group(1)] = {
                    "flow": int(m.group(2)),
                    "next": tuple(m.group(3).split(", ")),
                }
    return valves


def min_distance(valves, start, end):
    """
    >>> valves = read_input("input_example")
    >>> min_distance(valves, "AA", "DD")
    1
    >>> min_distance(valves, "AA", "CC")
    2
    >>> min_distance(valves, "AA", "GG")
    4
    """
    closed = []
    opn = [start]
    cost = {}
    cost[start] = 0

    while len(opn):
        opn.sort(key=lambda x: cost[x], reverse=True)
        cur = opn.pop()

        if cur == end:
            return cost[cur]
        for nxt in valves[cur]["next"]:
            if nxt not in closed and cost.get(nxt, 0) < cost[cur] + 1:
                cost[nxt] = cost[cur] + 1
                opn.append(nxt)

            closed.append(cur)
    raise (666)


def run_forrest_run(valves):
    """
    >>> valves = read_input("input_example")
    >>> run_forrest_run(valves)
    1651
    """
    start = "AA"
    targets = {
        name: attrs["flow"] for name, attrs in valves.items() if attrs["flow"] != 0
    }
    opened_valves = []

    time_fromto = {}
    for src in ["AA"] + list(targets.keys()):
        for dst in targets.keys():
            if src == dst:
                continue
            if src not in time_fromto:
                time_fromto[src] = {}
            time_fromto[src][dst] = min_distance(valves, src, dst)

    opn = [start]
    flow = {start: {"val": 0, "timeleft": 31}}
    while len(opn):
        opn.sort(key=lambda x: flow[x]["val"])
        path_key = opn.pop()
        path = path_key.split("-")
        cur = path[-1]

        for nxt in sorted(targets.keys(), key=lambda x: targets[x]):
            if nxt == cur or nxt in path:
                continue

            dst_nxt = time_fromto[cur][nxt]
            path_nxt = path + [nxt]
            path_key_nxt = "-".join(path_nxt)
            time_nxt = flow[path_key]["timeleft"] - dst_nxt - 1  # -1 to open the valve
            flow_nxt = (
                flow[path_key]["val"] + (time_nxt - 1) * targets[nxt]
            )  # time_nxt - 1 is the time the valve will be open

            if time_nxt > 0:
                flow[path_key_nxt] = {"val": flow_nxt, "timeleft": time_nxt}
                releasing = sum(targets[v] for v in path if v != "AA")
                stropen = f"Valves {path} are open, releasing {releasing} pressure."
                opn.append("-".join(path + [nxt]))

    return max([path["val"] for path in flow.values()])


if __name__ == "__main__":
    valves = read_input("input_real")
    print(run_forrest_run(valves))
