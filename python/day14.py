from pathlib import Path
from dataclasses import dataclass
from enum import Enum

file = Path(__file__).parent.parent / "data" / "day14.txt"
raw = file.read_text().strip()


class Element(Enum):
    AIR = '.'
    ROCK = '#'
    SAND = 'o'


FALLPATH: list[tuple[int, int]] = [(0, 1), (-1, 1), (1, 1)]


MapType = dict[tuple[int, int], Element]

@dataclass
class Cave:
    map: MapType
    x_range: tuple[int, int]
    y_range: tuple[int, int]
    start: tuple[int, int] = (500, 0)

    @classmethod
    def parse(cls, data: str):
        m: MapType = {}
        xmin = float('inf')
        ymin = float('inf')
        xmax = float('-inf')
        ymax = float('-inf')
        for line in data.splitlines():
            parts = line.split('->')
            for start, end in zip(parts, parts[1:]):
                a, b = map(int, start.split(','))
                c, d = map(int, end.split(','))
                if a == c:
                    small = min(b, d)
                    big = max(b, d)
                    for i in range(small, big + 1):
                        m[(a, i)] = Element.ROCK
                        xmin = min(a, xmin)
                        xmax = max(a, xmax)
                        ymin = min(i, ymin)
                        ymax = max(i, ymax)
                elif b == d:
                    small = min(a, c)
                    big = max(a, c)
                    for i in range(small, big + 1):
                        m[(i, b)] = Element.ROCK
                        xmin = min(i, xmin)
                        xmax = max(i, xmax)
                        ymin = min(b, ymin)
                        ymax = max(b, ymax)
        return cls(map=m, x_range=(int(xmin), int(xmax)), y_range=(int(ymin), int(ymax)))

    def draw(self, pad=10):
        rows = []
        for y in range(self.y_range[0] - pad, self.y_range[1] + 1 + pad):
            rows.append(''.join(self.map.get((x, y), Element.AIR).value for x in range(self.x_range[0] - pad, self.x_range[1] + 1 + pad)))
        return '\n'.join(rows)

    def step(self):
        return self.find_resting_point(self.start)

    def step_until_finished(self):
        while point := self.step():
            self.map[point] = Element.SAND
            if point == self.start:
                break

    def find_resting_point(self, point: tuple[int, int]) -> tuple[int, int] | None:
        if point[1] > self.y_range[1]:
            return None
        for vector in FALLPATH:
            dx, dy = vector
            npoint = point[0] + dx, point[1] + dy
            if self.map.get(npoint, Element.AIR) == Element.AIR:
                return self.find_resting_point(npoint)
        return point


class CaveWithFloor(Cave):
    def find_resting_point(self, point: tuple[int, int]) -> tuple[int, int] | None:
        if point[1] == self.y_range[1] + 1:
            return point
        for vector in FALLPATH:
            dx, dy = vector
            npoint = point[0] + dx, point[1] + dy
            if self.map.get(npoint, Element.AIR) == Element.AIR:
                return self.find_resting_point(npoint)
        return point


cave = Cave.parse(raw)
cave.step_until_finished()
print(len([x for x in cave.map.values() if x == Element.SAND]))

cave = CaveWithFloor.parse(raw)
cave.step_until_finished()
print(len([x for x in cave.map.values() if x == Element.SAND]))
