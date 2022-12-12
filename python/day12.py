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
    end: Point

    @classmethod
    def parse(cls, data: str):
        m: dict[Point, str] = {}
        start = Point(x=0, y=0)
        end = Point(x=0, y=0)
        for y, row in enumerate(data.splitlines()):
            for x, ch in enumerate(row):
                if ch == "S":
                    start = Point(x=x, y=y)
                elif ch == "E":
                    end = Point(x=x, y=y)
                m[Point(x=x, y=y)] = ch
        return cls(map=m, start=start, end=end)

    def find_end(self, start, backwards=False):
        queue: Queue[tuple[Point, int]] = Queue()
        queue.put((start, 0))
        visited: dict[Point, int] = {}
        end = 'aS' if backwards else 'E'
        while not queue.empty():
            point, dist = queue.get()
            if self.map[point] in end:
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
                if backwards:
                    if other_height >= height - 1:
                        queue.put((other, dist+1))
                else:
                    if other_height <= height + 1:
                        queue.put((other, dist + 1))
        return float("inf")


hill = Hill.parse(raw)
print(hill.find_end(hill.start))
print(hill.find_end(hill.end, backwards=True))
