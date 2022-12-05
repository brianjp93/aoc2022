from pathlib import Path
import re
from collections import defaultdict

file = Path(__file__).parent.parent / "data" / "day5.txt"
raw = file.read_text()

crate_string, arrangement = raw.split('\n\n')
lines = crate_string.splitlines()

def get_crates(lines: list[str]):
    crates: dict[int, list[str]] = defaultdict(list)
    for line in lines[:-1]:
        for i, idx in enumerate(range(1, len(lines[-1]), 4)):
            if ch := line[idx].strip():
                crates[i+1].insert(0, ch)
    return crates

def move(crates: dict[int, list[str]], group=False):
    for data in re.findall(r"move (\d+) from (\d+) to (\d+)", arrangement):
        count, start, end = map(int, data)
        piece = crates[start][-count:] if group else reversed(crates[start][-count:])
        crates[end].extend(piece)
        del crates[start][-count:]
    return "".join(crates[i][-1] for i in range(1, 10))


print(move(get_crates(lines)))
print(move(get_crates(lines), True))
