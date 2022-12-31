from enum import Enum
from pathlib import Path
from dataclasses import dataclass
import re
from typing import Self

from sympy.core.cache import cached_property

file = Path(__file__).parent.parent / "data" / "day22.txt"
raw = file.read_text()


class Space(Enum):
    OPEN = "."
    WALL = "#"
    ABYSS = ' '


DIRECTIONS: list[tuple[int, int]] = [(1, 0), (0, 1), (-1, 0), (0, -1)]


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


MapType = dict[Point, Space]


@dataclass
class Jungle:
    map: MapType
    row_ranges: dict[int, tuple[int, int]]
    col_ranges: dict[int, tuple[int, int]]
    start: Point
    instructions: list[tuple[str, int]]
    data: str

    @staticmethod
    def get_ranges(data: str):
        row_ranges: dict[int, tuple[int, int]] = {}
        col_ranges: dict[int, tuple[int, int]] = {}
        for y, row in enumerate(data.splitlines()):
            minx = float("inf")
            maxx = -float("inf")
            for x, ch in enumerate(row):
                if ch in (Space.OPEN.value, Space.WALL.value):
                    minx = min(x, minx)
                    maxx = max(x, maxx)
                    if x not in col_ranges:
                        col_ranges[x] = (1000000, -1)
                    col_ranges[x] = (min(col_ranges[x][0], y), max(col_ranges[x][1], y))
            row_ranges[y] = (int(minx), int(maxx))
        return row_ranges, col_ranges

    @classmethod
    def parse(cls, raw_data: str):
        data, instr = raw_data.split("\n\n")
        m: MapType = {}
        for y, row in enumerate(data.splitlines()):
            for x, ch in enumerate(row):
                match ch:
                    case Space.WALL.value:
                        m[Point(x, y)] = Space.WALL
                    case Space.OPEN.value:
                        m[Point(x, y)] = Space.OPEN
        row_ranges, col_ranges = cls.get_ranges(data)
        instrs = [
            (direction, int(count))
            for direction, count in re.findall(r"([RL])?(\d+)", instr)
        ]
        return cls(
            map=m,
            row_ranges=row_ranges,
            col_ranges=col_ranges,
            start=Point(row_ranges[0][0], 0),
            instructions=instrs,
            data=data,
        )

    def do_instructions(self):
        pos = self.start
        facing = 0
        for turn, count in self.instructions:
            if turn and turn in 'RL':
                d_facing = -1 if turn == 'L' else 1
                facing = (facing + d_facing) % len(DIRECTIONS)
            move = DIRECTIONS[facing]
            for _ in range(count):
                move = DIRECTIONS[facing]
                npos = pos + move
                nfacing = facing
                if self.map.get(npos, Space.ABYSS) == Space.ABYSS:
                    npos, nfacing = self.get_connection(npos, facing)
                if self.map.get(npos, Space.WALL) == Space.WALL:
                    break
                pos = npos
                facing = nfacing
        password = (1000 * (pos.y + 1)) + (4 * (pos.x + 1)) + facing
        return password

    def get_connection(self, pos: Point, facing: int):
        move = DIRECTIONS[facing]
        if move[0] > 0:
            low_x = self.row_ranges[pos.y][0]
            wrap = (low_x, pos.y)
        elif move[0] < 0:
            high_x = self.row_ranges[pos.y][1]
            wrap = (high_x, pos.y)
        elif move[1] > 0:
            wrap = (pos.x, self.col_ranges[pos.x][0])
        elif move[1] < 0:
            wrap = (pos.x, self.col_ranges[pos.x][1])
        else:
            raise Exception
        npos = Point(x=wrap[0], y=wrap[1])
        return npos, facing

    def draw(self, pos: Point):
        xmax = max(x[1] for x in self.row_ranges.values())
        ymax = max(x[1] for x in self.col_ranges.values())
        rows = []
        for y in range(ymax + 1):
            row = []
            for x in range(xmax + 1):
                if x == pos.x and y == pos.y:
                    row.append('o')
                else:
                    row.append(self.map.get(Point(x, y), Space.ABYSS).value)
            rows.append(''.join(row))
        return '\n'.join(rows)


class JungleCube(Jungle):
    def get_connection(self, pos: Point, facing: int):
        section = self.section(pos)
        match [section, facing]:
            # g
            case [-2, 3]:
                facing = 0
                x = 0
                y = (pos.x % self.block_size) + (self.block_size * 3)
                npos = Point(x, y)
            case [8, 2]:
                facing = 1
                y = 0
                x = (pos.y % self.block_size) + self.block_size
                npos = Point(x, y)
            # a
            case [-1, 3]:
                y = (self.block_size * 4) - 1
                x = (pos.x % self.block_size)
                npos = Point(x, y)
            case [12, 1]:
                y = 0
                x = (self.block_size * 2) + pos.x
                npos = Point(x, y)
            # b
            case [3, 0]:
                # flips
                facing = 2
                y = (self.block_size - pos.y - 1) + (self.block_size * 2)
                x = (self.block_size * 2) - 1
                npos = Point(x, y)
            case [8, 0]:
                # flips
                facing = 2
                x = (self.block_size * 3) - 1
                y_flip = self.block_size - (pos.y % self.block_size) - 1
                y = y_flip
                npos = Point(x, y)
            # c
            case [5, 1]:
                facing = 2
                x = (self.block_size * 2) - 1
                y = (pos.x % self.block_size) + self.block_size
                npos = Point(x, y)
            case [5, 0]:
                facing = 3
                y = self.block_size - 1
                x = (pos.y % self.block_size) + (2 * self.block_size)
                npos = Point(x, y)
            # d
            case [10, 1]:
                facing = 2
                x = self.block_size - 1
                y = (pos.x % self.block_size) + (self.block_size * 3)
                npos = Point(x, y)
            case [10, 0]:
                facing = 3
                y = (self.block_size * 3) - 1
                x = (pos.y % self.block_size) + self.block_size
                npos = Point(x, y)
            # e
            case [3, 2]:
                facing = 1
                y = (self.block_size * 2)
                x = (pos.y % self.block_size)
                npos = Point(x, y)
            case [3, 3]:
                facing = 0
                x = self.block_size
                y = pos.x + self.block_size
                npos = Point(x, y)
            # f
            case [0, 2]:
                facing = 0
                y_flip = self.block_size - pos.y - 1
                y = y_flip + (2 * self.block_size)
                x = 0
                npos = Point(x, y)
            case [5, 2]:
                facing = 0
                x = self.block_size
                y_flip = self.block_size - (pos.y % self.block_size) - 1
                y = y_flip
                npos = Point(x, y)
            case _:
                raise RuntimeError('you have made a mistake')
        return npos, facing

    @cached_property
    def block_size(self):
        return len(self.data.splitlines()[0]) // 3

    def section(self, pos: Point):
        size: int = self.block_size
        x = pos.x // size
        y = pos.y // size
        return (y * 3) + x

jungle = Jungle.parse(raw)
password = jungle.do_instructions()
print(f'Part1: {password}')

jc = JungleCube.parse(raw)
password = jc.do_instructions()
print(f'Part2: {password}')
