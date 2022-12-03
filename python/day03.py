from pathlib import Path
from string import ascii_letters

file = Path(__file__).parent.parent / "data" / "day3.txt"
raw = file.read_text().strip()
data = [x for x in raw.splitlines()]

def score(args):
    return ascii_letters.index(set.intersection(*map(set, args)).pop()) + 1

print(sum(score([x[:len(x)//2], x[len(x)//2:]]) for x in data))
print(sum(score(data[i:i+3]) for i in range(0, len(data), 3)))
