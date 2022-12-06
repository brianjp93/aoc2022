from pathlib import Path

file = Path(__file__).parent.parent / "data" / "day6.txt"
raw = file.read_text().strip()

def find_start(count: int):
    for i in range(len(raw)):
        x = set(raw[i:i+count])
        if len(x) == count:
            return i + count

print(f'part 1: {find_start(4)}')
print(f'part 1: {find_start(14)}')
