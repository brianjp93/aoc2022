from pathlib import Path
import re

file = Path(__file__).parent.parent / "data" / "day5.txt"
raw = file.read_text()

CRATE_STRING, ARRANGEMENT = raw.split('\n\n')
LINES = CRATE_STRING.splitlines()

def get_crates():
    for idx in range(1, len(LINES[-1]), 4):
        yield [x[idx] for x in LINES[:-1] if x[idx].strip()][::-1]

def get_instructions():
    for data in re.findall(r"move (\d+) from (\d+) to (\d+)", ARRANGEMENT):
        count, start, end = map(int, data)
        yield count, start-1, end-1

def move(crates: list[list[str]], group=False):
    for count, start, end in get_instructions():
        piece = crates[start][-count:] if group else crates[start][-count:][::-1]
        crates[end].extend(piece)
        del crates[start][-count:]
    return "".join(x[-1] for x in crates)


print(move(list(get_crates())))
print(move(list(get_crates()), True))
