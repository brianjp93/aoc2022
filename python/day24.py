from functools import cached_property
from pathlib import Path
from dataclasses import dataclass, field
from typing import Literal, Self
from queue import PriorityQueue
from math import lcm


file = Path(__file__).parent.parent / "data" / "day24.txt"
raw = file.read_text()

OPEN = "."
WALL = "#"

BLIZZARDS: dict[Literal["^", ">", "<", "v"], tuple[int, int]] = {
    "v": (0, 1),
    ">": (1, 0),
    "^": (0, -1),
    "<": (-1, 0),
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


@dataclass(order=True)
class Item:
    heuristic: int
    t: int
    pos: Point = field(compare=False)


@dataclass(frozen=True)
class Basin:
    map: dict[Point, str] = field(hash=False)
    start: Point
    end: Point
    x_length: int
    y_length: int
    map_cache: dict[int, dict[Point, str]] = field(default_factory=dict)

    @classmethod
    def parse(cls, data: str):
        m = {}
        start = None
        end = None
        lines = data.splitlines()
        x_length = len(lines[0]) - 2
        y_length = len(lines) - 2
        for y, row in enumerate(lines):
            y = y - 1
            for x, ch in enumerate(row):
                x = x - 1
                if ch in ".^v<>":
                    m[Point(x, y)] = ch
                    if y == -1:
                        if ch == ".":
                            start = Point(x, y)
                    elif y == y_length:
                        if ch == ".":
                            end = Point(x, y)
        assert start and end
        return cls(map=m, start=start, x_length=x_length, y_length=y_length, end=end)

    @cached_property
    def tmod(self):
        return lcm(self.x_length, self.y_length)

    def dist(self, pos: Point):
        return abs(pos.x - self.end.x) + abs(pos.y - self.end.y)

    def back_and_forth(self):
        t1 = self.traverse(self.start, self.end)
        t2 = self.traverse(self.end, self.start, init_t=t1)
        t3 = self.traverse(self.start, self.end, init_t=t2)
        return t3

    def traverse(self, start: Point, end: Point, init_t=0):
        queue: PriorityQueue[Item] = PriorityQueue()
        queue.put(Item(heuristic=self.dist(start), t=init_t, pos=start))
        min_t = float("inf")
        out = None
        visited: dict[tuple[Point, int], int] = {}
        while not queue.empty():
            item = queue.get()
            heur, t, pos = item.heuristic, item.t, item.pos
            key = (item.pos, t % self.tmod)
            if other_t := visited.get(key, None):
                if t >= other_t:
                    continue
            else:
                visited[key] = t

            m = self.calculate_map(t)
            if m[pos] in BLIZZARDS.keys():
                continue

            if heur >= min_t:
                continue

            if pos == end:
                if t < min_t:
                    min_t = t
                    out = t
                continue

            nt = t + 1
            queue.put(Item(heuristic=heur + 1, t=nt, pos=pos))
            for adj in BLIZZARDS.values():
                npos = pos + adj
                if npos in self.map:
                    queue.put(Item(heuristic=nt + self.dist(npos), t=nt, pos=npos))
        assert out
        return out

    def draw(self, pos: Point, t: int):
        m = self.calculate_map(t)
        rows = []
        for y in range(-1, self.y_length + 1):
            row = []
            for x in range(-1, self.x_length + 1):
                point = Point(x, y)
                if pos == point:
                    row.append("O")
                elif point == self.end:
                    row.append("E")
                elif point == self.start:
                    row.append("S")
                else:
                    row.append(m.get(point, WALL))
            rows.append("".join(row))
        print("\n".join(rows))

    def draw_path(self, moves: list[Point]):
        for t, pos in enumerate(moves):
            self.draw(pos, t)
            input()

    def calculate_map(self, t: int):
        t = t % self.tmod
        if ret := self.map_cache.get(t, None):
            return ret
        m: dict[Point, str] = {}
        for point, val in self.map.items():
            if val in "<>v^.":
                m[point] = "."
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
                m[npoint] = val
        self.map_cache[t] = m
        return m


def part1():
    basin = Basin.parse(raw)
    t = basin.traverse(basin.start, basin.end)
    return t


def part2():
    basin = Basin.parse(raw)
    t = basin.back_and_forth()
    return t


print(f'{part1()=}')
print(f"{part2()=}")
