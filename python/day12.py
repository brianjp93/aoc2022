from dataclasses import dataclass
from pathlib import Path
from string import ascii_lowercase
from queue import Queue

ASCII = {ch: i for i, ch in enumerate(ascii_lowercase)}
ASCII["S"] = ASCII["a"]
ASCII["E"] = ASCII["z"]

file = Path(__file__).parent.parent / "data" / "day12.txt"
raw = file.read_text().strip()


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def __add__(self, other):
        return Point(x=self.x + other.x, y=self.y + other.y)

    def __sub__(self, other):
        return Point(x=self.x - other.x, y=self.y - other.y)


DIRS = [Point(x=1, y=0), Point(x=-1, y=0), Point(x=0, y=-1), Point(x=0, y=1)]


@dataclass
class Hill:
    map: dict[Point, str]
    start: Point

    @classmethod
    def parse(cls, data: str):
        m: dict[Point, str] = {}
        start = Point(x=0, y=0)
        for y, row in enumerate(data.splitlines()):
            for x, ch in enumerate(row):
                if ch == "S":
                    start = Point(x=x, y=y)
                m[Point(x=x, y=y)] = ch
        return cls(map=m, start=start)

    @property
    def all_starts(self):
        return [point for point, ch in self.map.items() if ch in "Sa"]

    def find_end(self, start):
        queue: Queue[tuple[Point, int]] = Queue()
        queue.put((start, 0))
        visited: dict[Point, int] = {}
        while not queue.empty():
            point, dist = queue.get()
            if self.map[point] == "E":
                return dist
            if found := visited.get(point, None):
                if dist >= found:
                    continue
            else:
                visited[point] = dist
            height = ASCII[self.map[point]]
            for d in DIRS:
                other = point + d
                other_val = self.map.get(other, None)
                if other_val is None:
                    continue
                other_height = ASCII[other_val]
                if other_height <= height + 1:
                    queue.put((other, dist + 1))
        return float("inf")

    def find_most_difficult_rock_climibing_trail_for_some_reason(self):
        return min(*[self.find_end(x) for x in self.all_starts])


hill = Hill.parse(raw)
print(hill.find_end(hill.start))
print(hill.find_most_difficult_rock_climibing_trail_for_some_reason())
