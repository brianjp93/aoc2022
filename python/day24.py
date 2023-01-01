from collections import defaultdict
from functools import cache
from itertools import count, product
from pathlib import Path
from dataclasses import dataclass, field
from typing import Literal, Self, Type
from queue import PriorityQueue


file = Path(__file__).parent.parent / "data" / "day24.txt"
raw = file.read_text()


#raw = """
##.######
##>>.<^<#
##.<..<<#
##>v.><>#
##<^v^^>#
#######.#""".strip()

OPEN = '.'
WALL = '#'

BLIZZARDS: dict[Literal['^', '>', '<', 'v'], tuple[int, int]] = {
    'v': (0, 1),
    '>': (1, 0),
    '^': (0, -1),
    '<': (-1, 0),
}
BLIZZARD_KEYS = set(BLIZZARDS.keys())

rbliz = {
    val: key for key, val in BLIZZARDS.items()
}


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

    def as_tuple(self):
        return (self.x, self.y)


@dataclass(order=True)
class Item:
    t: int
    dist: int
    pos: Point = field(compare=False)
    moves: list[Point] = field(compare=False)


@dataclass(frozen=True)
class Basin:
    map: dict[Point, str] = field(hash=False)
    start: Point
    end: Point
    x_length: int
    y_length: int

    @classmethod
    def parse(cls, data: str):
        m = {}
        start = None
        end = None
        lines = data.splitlines()
        x_length = len(lines[0]) - 2
        y_length = len(lines) - 2
        print(f'{x_length=}')
        print(f'{y_length=}')
        for y, row in enumerate(lines):
            y = y - 1
            for x, ch in enumerate(row):
                x = x - 1
                if ch in '.^v<>':
                    m[Point(x, y)] = ch
                    if y == -1:
                        if ch == '.':
                            start = Point(x, y)
                    elif y == y_length:
                        if ch == '.':
                            end = Point(x, y)
        assert start and end
        return cls(map=m, start=start, x_length=x_length, y_length=y_length, end=end)

    def dist(self, pos: Point):
        dx = abs(pos.x - self.end.x)
        dy = abs(pos.y - self.end.y)
        return dx + dy

    def traverse(self):
        queue: PriorityQueue[Item] = PriorityQueue()
        queue.put(Item(t=0, dist=self.dist(self.start), pos=self.start, moves=[self.start]))
        min_t = float('inf')
        out = None
        while not queue.empty():
            item = queue.get()
            t, dist, pos, moves = item.t,  item.dist, item.pos, item.moves
            m = self.calculate_map(t)
            if m[pos] in BLIZZARD_KEYS:
                continue

            if t + dist >= min_t:
                continue

            if pos == self.end:
                # print(moves)
                if t < min_t:
                    print(f'Found path with time {t}')
                    # print(moves)
                    # self.draw_path(moves)
                    min_t = t
                    out = t, moves
                continue

            nt = t + 1
            queue.put(Item(t=nt, dist=dist, pos=pos, moves=moves[:] + [pos]))
            for adj in BLIZZARDS.values():
                npos = pos + adj
                if self.map.get(npos, WALL) != WALL:
                    queue.put(Item(t=nt, dist=self.dist(npos), pos=npos, moves=moves[:] + [npos]))
        assert out
        return out

    def draw(self, pos: Point, t: int):
        print(f'{t=}')
        m = self.calculate_map(t)
        rows = []
        for y in range(-1, self.y_length + 1):
            row = []
            for x in range(-1, self.x_length + 1):
                point = Point(x, y)
                if pos == point:
                    row.append('O')
                elif point == self.end:
                    row.append('E')
                elif point == self.start:
                    row.append('S')
                else:
                    row.append(m.get(point, WALL))
            rows.append(''.join(row))
        print('\n'.join(rows))

    def draw_path(self, moves: list[Point]):
        for t, pos in enumerate(moves):
            self.draw(pos, t)
            input()

    @cache
    def calculate_map(self, t: int):
        m: dict[Point, str] = {}
        for point, val in self.map.items():
            if val in '<>v^.':
                m[point] = '.'
        for point, val in self.map.items():
            if move := BLIZZARDS.get(val, None):  # type: ignore
                idx = (move.index(0) + 1) % 2
                if idx == 0:
                    x0 = point.x
                    y = point.y
                    x = ((move[idx] * t) + x0) % self.x_length
                else:
                    y0 = point.y
                    x = point.x
                    y = ((move[idx] * t) + y0) % self.y_length
                npoint = Point(x, y)
                # print(f'{val=}, start={point}, {t=}, calculated: {npoint}')
                m[npoint] = val
        return m


basin = Basin.parse(raw)
# print(basin)
t, moves = basin.traverse()
print(t)


# basin = Basin.parse(raw)
# for t in range(20):
#     basin.draw(Point(-1, -1), t)
#     input()
