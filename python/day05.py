from pathlib import Path
import re

file = Path(__file__).parent.parent / "data" / "day5.txt"
raw = file.read_text()

crate_string, arrangement = raw.split('\n\n')
lines = crate_string.splitlines()

def get_crates(lines: list[str]):
    for idx in range(1, len(lines[-1]), 4):
        yield [x[idx] for x in lines[:-1] if x[idx].strip()][::-1]

def move(crates: list[list[str]], group=False):
    for data in re.findall(r"move (\d+) from (\d+) to (\d+)", arrangement):
        count, start, end = map(int, data)
        start, end = start-1, end-1
        piece = crates[start][-count:] if group else crates[start][-count:][::-1]
        crates[end].extend(piece)
        del crates[start][-count:]
    return "".join(x[-1] for x in crates)


print(move(list(get_crates(lines))))
print(move(list(get_crates(lines)), True))
