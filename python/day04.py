from pathlib import Path
import re

file = Path(__file__).parent.parent / "data" / "day4.txt"
raw = file.read_text().strip()

count = 0
count2 = 0
for x in re.findall(r'(\d+)-(\d+),(\d+)-(\d+)', raw):
    a, b, c, d = map(int, x)
    s1 = set(range(a, b + 1))
    s2 = set(range(c, d + 1))
    if len(s1.union(s2)) == max(len(s1), len(s2)):
        count += 1
    if len(s1 & s2) > 0:
        count2 += 1

print(count)
print(count2)
