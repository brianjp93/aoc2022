from pathlib import Path

file = Path(__file__).parent.parent / "data" / "day9.txt"
raw = file.read_text().strip()

DIR: dict[str, complex] = {
    "U": -1j,
    "D": 1j,
    "R": 1,
    "L": -1,
}

class Rope:
    def __init__(self, instructions: str, length=2):
        self.rope = [0j]*length
        self.instructions = list(self.parse(instructions))
        self.l_history = set()

    def parse(self, data: str):
        for line in data.splitlines():
            a, b = line.split()
            b = int(b)
            yield a, b

    def do_moves(self):
        for (direction, count) in self.instructions:
            self.do_move(direction, count)

    def do_move(self, direction: str, count: int):
        for _ in range(count):
            self.rope[0] += DIR[direction]
            for i in range(len(self.rope)-1):
                h, l = self.rope[i:i+2]
                l = self.follow(h, l)
                self.rope[i+1] = l
            self.l_history.add(self.rope[-1])

    def follow(self, h: complex, l: complex):
        diff = h - l
        dx, dy = diff.real, diff.imag
        dx_unit = abs(dx) / dx if dx else 0
        dy_unit = complex(0, abs(dy) / dy) if dy else 0
        if abs(dx) == 2:
            l += dx_unit
            if abs(dy) >= 1:
                l += dy_unit
        elif abs(dy) == 2:
            l += dy_unit
            if abs(dx) >= 1:
                l += dx_unit
        return l


if __name__ == '__main__':
    rope = Rope(raw, length=2)
    rope.do_moves()
    print(len(rope.l_history))

    rope = Rope(raw, length=10)
    rope.do_moves()
    print(len(rope.l_history))
