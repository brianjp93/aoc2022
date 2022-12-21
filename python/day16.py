from pathlib import Path
import re
from itertools import product

file = Path(__file__).parent.parent / "data" / "day16.txt"
raw = file.read_text().strip()

# raw = """Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
# Valve BB has flow rate=13; tunnels lead to valves CC, AA
# Valve CC has flow rate=2; tunnels lead to valves DD, BB
# Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
# Valve EE has flow rate=3; tunnels lead to valves FF, DD
# Valve FF has flow rate=0; tunnels lead to valves EE, GG
# Valve GG has flow rate=0; tunnels lead to valves FF, HH
# Valve HH has flow rate=22; tunnel leads to valve GG
# Valve II has flow rate=0; tunnels lead to valves AA, JJ
# Valve JJ has flow rate=21; tunnel leads to valve II"""

ValveMap = dict[str, tuple[int, set[str]]]


def parse(data: str):
    valves: ValveMap = {}
    for name, rate, to_valves in re.findall(r'Valve (\w+).*?(\d+).*?valve[s]? (.+)', data):
        to_valves: str
        rate = int(rate)
        to_valve_set = {x.strip() for x in to_valves.split(',')}
        valves[name] = (rate, to_valve_set)
    return valves

VALVES = parse(raw)
VALVE_KEYS = set(VALVES.keys())
NEED_TO_OPEN = set(a for a, b in VALVES.items() if b[0] > 0)
START = 'AA'

def traverse():
    stack: list[tuple[str, str|None, dict[str, int], int]] = [(START, None, {}, 30)]
    maximum = 0
    # inspected = 0
    while stack:
        # inspected += 1
        # if inspected % 1_000_000 == 0:
        #     print(f'nodes inspected: {inspected}')
        valve, prev, opened, minutes = stack.pop()

        valves_left = NEED_TO_OPEN - opened.keys()
        valves_left_values = [VALVES[x][0] for x in valves_left]
        valves_left_values.sort(reverse=True)
        max_possible = sum(x * max(minutes - (i*2), 0) for i, x in enumerate(valves_left_values)) + sum(opened.values())

        if max_possible <= maximum:
            continue

        if minutes <= 1 or len(valves_left) == 0:
            maximum = max(maximum, sum(opened.values()))
            continue
        rate, to_valves = VALVES[valve]
        next_minutes = minutes - 1
        if valve not in opened and rate > 0:
            # open valve
            next_opened = opened.copy()
            next_opened[valve] = next_minutes * rate
            stack.append((valve, valve, next_opened, next_minutes))
        for next_valve in to_valves:
            # don't open valve
            if next_valve != prev:
                stack.append((next_valve, valve, opened.copy(), next_minutes))
    return maximum


def double_traverse():
    stack: list[tuple[str, str, str|None, str|None, dict[str, int], int]] = [(START, START, None, None, {}, 26)]
    maximum = 0
    # inspected = 0
    while stack:
        # inspected += 1
        # if inspected % 1_000_000 == 0:
        #     print(f'nodes inspected: {inspected}')
        valve1, valve2, prev1, prev2, opened, minutes = stack.pop()

        valves_left = NEED_TO_OPEN - opened.keys()
        valves_left_values = [VALVES[x][0] for x in valves_left]
        valves_left_values.sort(reverse=True)
        max_possible = sum(x * max(minutes - ((i//2)*2), 0) for i, x in enumerate(valves_left_values)) + sum(opened.values())

        if max_possible <= maximum:
            continue

        if minutes <= 1 or len(valves_left) == 0:
            maximum = max(maximum, sum(opened.values()))
            continue

        rate1, to_valves1 = VALVES[valve1]
        rate2, to_valves2 = VALVES[valve2]
        to_valves2 = to_valves2 - {prev1, prev2, valve1}
        to_valves1 = to_valves1 - {prev1, prev2, valve2}
        next_minutes = minutes - 1
        if rate1 > 0 and valve1 not in opened:
            for next_valve2 in to_valves2:
                # open valve1 only
                next_opened = opened.copy()
                next_opened[valve1] = next_minutes * rate1
                stack.append((valve1, next_valve2, valve1, valve2, next_opened, next_minutes))
        if rate2 > 0 and valve2 not in opened:
            for next_valve1 in to_valves1:
                # open valve2 only
                next_opened = opened.copy()
                next_opened[valve2] = next_minutes * rate2
                stack.append((next_valve1, valve2, valve1, valve2, next_opened, next_minutes))
        if rate1 != 0 and rate2 != 0 and valve1 != valve2 and valve1 not in opened and valve2 not in opened:
            # open both valves
            next_opened = opened.copy()
            next_opened[valve1] = next_minutes * rate1
            next_opened[valve2] = next_minutes * rate2
            stack.append((valve1, valve2, valve1, valve2, next_opened, next_minutes))
        for next_valve1, next_valve2 in product(to_valves1, to_valves2):
            # don't open either valve
            stack.append((next_valve1, next_valve2, valve1, valve2, opened.copy(), next_minutes))
    return maximum


# print(VALVES)

out = traverse()
print(out)

out = double_traverse()
print(out)
