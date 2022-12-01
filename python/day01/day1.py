from pathlib import Path
file = Path(__file__).parent.parent.parent / 'data' / 'day1.txt'
x = sorted(
    [sum(map(int, x.split())) for x in file.read_text().split('\n\n')],
    reverse=True
)
print(x[0])
print(sum(x[:3]))
