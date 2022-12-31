from collections import defaultdict
from itertools import count, product
from pathlib import Path
from dataclasses import dataclass, field
from typing import Self


file = Path(__file__).parent.parent / "data" / "day23.txt"
raw = file.read_text()


BIG = 10000000000
SMALL = -10000000000


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def __add__(self, other: Self | tuple[int, int]):
        x, y = other if isinstance(other, tuple) else (other.x, other.y)
        return Point(x=self.x + x, y=self.y + y)

    def __sub__(self, other: Self | tuple[int, int]):
        x, y = other if isinstance(other, tuple) else (other.x, other.y)
        return Point(x=self.x - x, y=self.y - y)


MOVES = [(0, -1), (0, 1), (-1, 0), (1, 0)]
ADJ = list(product((1, -1, 0), repeat=2))
ADJ.remove((0, 0))


@dataclass
class Crater:
    map: set[Point]
    moves: list[tuple[int, int]] = field(default_factory=lambda: MOVES[:], repr=False)

    @classmethod
    def parse(cls, data: str):
        m = set()
        for y, row in enumerate(data.splitlines()):
            for x, ch in enumerate(row):
                if ch == '#':
                    m.add(Point(x, y))
        return cls(map=m)

    def is_all_adj_open(self, point: Point):
        for move in ADJ:
            npos = point + move
            if npos in self.map:
                return False
        return True

    def step(self):
        considerations: dict[Point, list[Point]] = defaultdict(list)
        moves = 0
        for point in self.map:
            if self.is_all_adj_open(point):
                continue

            for move in self.moves:
                idx = move.index(0)
                is_open = True
                for i in (-1, 0, 1):
                    nmove = list(move[:])
                    nmove[idx] = i
                    npos = point + tuple(nmove)
                    if npos in self.map:
                        is_open = False
                if is_open:
                    considerations[point + move].append(point)
                    break
        for point, considered_by in considerations.items():
            if len(considered_by) == 1:
                self.map.add(point)
                self.map.remove(considered_by[0])
                moves += 1
        x = self.moves.pop(0)
        self.moves.append(x)
        return moves

    def steps(self, count=10):
        for _ in range(count):
            self.step()

    def until_frozen(self):
        for i in count(1):
            moves = self.step()
            if moves == 0:
                return i

    def get_edges(self):
        minx = miny = BIG
        maxx = maxy = SMALL
        for point in self.map:
            minx = min(minx, point.x)
            maxx = max(maxx, point.x)
            miny = min(miny, point.y)
            maxy = max(maxy, point.y)
        return minx, maxx, miny, maxy

    def count_ground(self):
        minx, maxx, miny, maxy = self.get_edges()
        dx = maxx - minx + 1
        dy = maxy - miny + 1
        total = dx * dy
        ground = total - len(self.map)
        return ground

    def draw(self):
        minx, maxx, miny, maxy = self.get_edges()
        rows = []
        for y in range(miny, maxy + 1):
            row = []
            for x in range(minx, maxx + 1):
                if Point(x, y) in self.map:
                    row.append('#')
                else:
                    row.append('.')
            rows.append(''.join(row))
        print('\n'.join(rows))


crater = Crater.parse(raw)
crater.steps(10)
ground = crater.count_ground()
print(f'Part1: {ground}')

crater = Crater.parse(raw)
move = crater.until_frozen()
print(f'Part2: {move}')
