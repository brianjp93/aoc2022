from pathlib import Path
from dataclasses import dataclass


file = Path(__file__).parent.parent / "data" / "day17.txt"
raw = file.read_text().strip()

# raw = '>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>'
raw = raw.strip()

@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def __add__(self, other):
        return Point(x=self.x + other.x, y=self.y + other.y)

    def __sub__(self, other):
        return Point(x=self.x - other.x, y=self.y - other.y)


@dataclass
class Block:
    map: list[Point]

    @property
    def left(self):
        left = self.map[0]
        for point in self.map[1:]:
            if point.x < left.x:
                left = point
        return left

    @property
    def right(self):
        right = self.map[0]
        for point in self.map[1:]:
            if point.x > right.x:
                right = point
        return right

    @property
    def bottom(self):
        bottom = self.map[0]
        for point in self.map[1:]:
            if point.y < bottom.y:
                bottom = point
        return bottom

    def move(self, vector: Point):
        new_map: list[Point] = []
        for point in self.map:
            new_map.append(point + vector)
        self.map = new_map


FLAT = Block(map=[Point(0,0), Point(1, 0), Point(2, 0), Point(3, 0)])
PLUS = Block(map=[Point(1, 0), Point(0, 1), Point(1, 1), Point(2, 1), Point(1, 2)])
REV_L = Block(map=[Point(0, 0), Point(1, 0), Point(2, 0), Point(2, 1), Point(2, 2)])
LINE = Block(map=[Point(0, 0), Point(0, 1), Point(0, 2), Point(0, 3)])
SQUARE = Block(map=[Point(0, 0), Point(0, 1), Point(1, 0), Point(1, 1)])

ORDER = [FLAT, PLUS, REV_L, LINE, SQUARE]

MOVE_LEFT = Point(-1, 0)
MOVE_RIGHT = Point(1, 0)
MOVE_DOWN = Point(0, -1)
MOVE_UP = Point(0, 1)


@dataclass
class Chamber:
    map: set[Point]
    WALL_LEFT = -1
    WALL_RIGHT = 7
    GROUND = -1

    def run_simulation(self, rock_count=2022):
        rocks = 0
        block_step = 0
        block = None
        jet_step = 0
        while rocks < rock_count:
            if block is None:
                block = ORDER[block_step]
                block_step = (block_step + 1) % len(ORDER)
                self.init_block(block)
            jet_dir = raw[jet_step]
            jet = MOVE_RIGHT if jet_dir == '>' else MOVE_LEFT
            jet_step = (jet_step + 1) % len(raw)
            block.move(jet)
            if self.is_collision(block):
                block.move(Point(0, 0) - jet)
            block.move(MOVE_DOWN)
            if self.is_collision(block):
                block.move(MOVE_UP)
                for point in block.map:
                    self.map.add(point)
                block = None
                rocks += 1
            self.draw_map(block)
            input()

    def is_collision(self, block: Block):
        if block.left.x <= self.WALL_LEFT:
            return True
        if block.right.x >= self.WALL_RIGHT:
            return True
        if block.bottom.y <= self.GROUND:
            return True
        for point in block.map:
            if point in self.map:
                return True
        return False

    def init_block(self, block: Block):
        left = block.left
        xpoint = Point(2, left.y) - left
        bottom = block.bottom
        ypoint = Point(bottom.x, self.top_y + 4) - bottom
        move = xpoint + ypoint
        block.move(move)

    @property
    def top_y(self):
        top_y = -1
        for point in self.map:
            if point.y > top_y:
                top_y = point.y
        return top_y

    def draw_map(self, block: Block | None):
        top_y = self.top_y + 5
        rows = []
        for y in range(top_y + 1, self.GROUND, -1):
            row = []
            for x in range(0, self.WALL_RIGHT):
                point = Point(x, y)
                if point in self.map or (block is not None and point in block.map):
                    row.append('#')
                else:
                    row.append('.')
            rows.append(''.join(row))
        print('\n'.join(rows))
        print('\n-------------------\n')


chamber = Chamber(set())
chamber.run_simulation()
print(chamber.top_y + 1)

# repeat_point = 50455
# chamber.run_simulation(repeat_point)
# print(chamber.top_y + 1)
# rocks = 1_000_000_000_000
