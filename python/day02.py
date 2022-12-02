from pathlib import Path
file = Path(__file__).parent.parent / 'data' / 'day2.txt'
raw = file.read_text().strip()

choices: dict[str, int] = {
    'A': 0, 'X': 0,
    'B': 1, 'Y': 1,
    'C': 2, 'Z': 2,
}

Data = list[tuple[int, int]]
x: Data = [tuple(map(lambda a: choices[a], x.split())) for x in raw.splitlines()]


def get_score(data: Data, alt=False):
    score = 0
    for a, b in data:
        if alt:
            b = (a + (b + 2) % 3) % 3
        mod = (b - a) % 3
        score += (3 * (1 + mod)) % 9 + b + 1
    return score


print(get_score(x))
print(get_score(x, True))
