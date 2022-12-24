from pathlib import Path
from dataclasses import dataclass


file = Path(__file__).parent.parent / "data" / "day17.txt"
raw = file.read_text().strip()

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

    @property
    def top(self):
        top = self.map[0]
        for point in self.map[1:]:
            if point.y > top.y:
                top = point
        return top

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
    top_y = -1

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
                self.top_y = max(self.top_y, block.top.y)
                block = None
                rocks += 1

    def get_big_rocks(self, rock_count=1_000_000_000_000):
        rocks = 0
        block_step = 0
        block = None
        jet_step = 0
        last_height = 0
        last_rocks = 0
        cycle = dy_first = drock_first = offset_height = height_after_cycles = 0
        rocks_remaining = None
        end_rock_count = 0
        while True:
            if jet_step == 0:
                new_height = self.top_y + 1
                dy = new_height - last_height
                drocks = rocks - last_rocks
                last_rocks = rocks
                last_height = new_height
                if cycle == 1:
                    dy_first = dy
                    drock_first = drocks
                elif cycle == 2:
                    dy_cycle = dy
                    drock_cycle = drocks
                    rocks_left = rock_count - drock_first
                    cycles_left = rocks_left // drock_cycle
                    rocks_after_cycles = (drock_cycle * cycles_left) + drock_first
                    height_after_cycles = (dy_cycle * cycles_left) + dy_first
                    rocks_remaining = rock_count - rocks_after_cycles
                    offset_height = new_height
                    end_rock_count = 0
                cycle += 1
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
                self.top_y = max(self.top_y, block.top.y)
                block = None
                rocks += 1
                end_rock_count += 1
                if end_rock_count == rocks_remaining:
                    height_change = (self.top_y + 1) - offset_height
                    return height_change + height_after_cycles

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
chamber.run_simulation(2022)
print(chamber.top_y + 1)

chamber = Chamber(set())
out = chamber.get_big_rocks()
print(out)
