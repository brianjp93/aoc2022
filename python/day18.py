from collections import defaultdict
from pathlib import Path
from dataclasses import dataclass, field

file = Path(__file__).parent.parent / "data" / "day18.txt"
raw = file.read_text().strip()

ADJ = [
    (1, 0, 0),
    (-1, 0, 0),
    (0, 1, 0),
    (0, -1, 0),
    (0, 0, 1),
    (0, 0, -1),
]


@dataclass(frozen=True)
class Cube:
    x: int
    y: int
    z: int

    def adj(self):
        for dx, dy, dz in ADJ:
            yield self.__class__(self.x + dx, self.y + dy, self.z + dz)


@dataclass
class Space:
    cubes: set[Cube]
    x: dict[tuple[int, int], list[Cube]]
    y: dict[tuple[int, int], list[Cube]]
    z: dict[tuple[int, int], list[Cube]]
    min_x: int
    max_x: int
    min_y: int
    max_y: int
    min_z: int
    max_z: int
    bubbles: set[Cube] = field(default_factory=set)

    @classmethod
    def parse(cls, data: str):
        cubes = set()
        x: dict[tuple[int, int], list[Cube]] = defaultdict(list)
        y: dict[tuple[int, int], list[Cube]] = defaultdict(list)
        z: dict[tuple[int, int], list[Cube]] = defaultdict(list)
        min_x = float("inf")
        max_x = -float("inf")
        min_y = float("inf")
        max_y = -float("inf")
        min_z = float("inf")
        max_z = -float("inf")
        for line in data.splitlines():
            a, b, c = map(int, line.split(","))
            cube = Cube(a, b, c)
            cubes.add(cube)
            x[(cube.y, cube.z)].append(cube)
            y[(cube.x, cube.z)].append(cube)
            z[(cube.x, cube.y)].append(cube)
            min_x = min(cube.x, min_x)
            max_x = max(cube.x, max_x)
            min_y = min(cube.y, min_y)
            max_y = max(cube.y, max_y)
            min_z = min(cube.z, min_z)
            max_z = max(cube.z, max_z)
        for key, val in x.items():
            x[key] = sorted(val, key=lambda x: x.x)
        for key, val in y.items():
            y[key] = sorted(val, key=lambda y: y.y)
        for key, val in z.items():
            z[key] = sorted(val, key=lambda z: z.z)
        return cls(
            cubes,
            x=x,
            y=y,
            z=z,
            min_x=int(min_x),
            max_x=int(max_x),
            min_y=int(min_y),
            max_y=int(max_y),
            min_z=int(min_z),
            max_z=int(max_z),
        )

    def surface_area(self):
        count = 0
        for cube in self.cubes:
            for adj in cube.adj():
                if adj not in self.cubes:
                    count += 1
        return count

    def has_cube_all_sides(self, cube: Cube):
        x_cubes = self.x[(cube.y, cube.z)]
        if x_cubes:
            lt = x_cubes[0]
            gt = x_cubes[-1]
            if lt.x >= cube.x or gt.x <= cube.x:
                return False
        y_cubes = self.y[(cube.x, cube.z)]
        if y_cubes:
            lt = y_cubes[0]
            gt = y_cubes[-1]
            if lt.y >= cube.y or gt.y <= cube.y:
                return False
        z_cubes = self.z[(cube.x, cube.y)]
        if z_cubes:
            lt = z_cubes[0]
            gt = z_cubes[-1]
            if lt.z >= cube.z or gt.z <= cube.z:
                return False
        return True

    def external_surface_area(self):
        count = 0
        for cube in self.cubes:
            for adj in cube.adj():
                if adj not in self.cubes:
                    if self.has_cube_all_sides(adj):
                        flooded = self.flood(adj)
                        if not flooded:
                            count += 1
                        self.bubbles |= flooded
                    else:
                        count += 1
        return count

    def flood(self, cube: Cube) -> set[Cube]:
        stack = [cube]
        flooded: set[Cube] = set()
        while stack:
            item = stack.pop()
            if item in self.bubbles:
                return self.bubbles
            if item.x < self.min_x or item.x > self.max_x:
                return set()
            elif item.y < self.min_y or item.y > self.max_y:
                return set()
            elif item.z < self.min_z or item.z > self.max_z:
                return set()
            flooded.add(item)
            for other in item.adj():
                if other not in self.cubes and other not in flooded:
                    stack.append(other)
        return flooded


space = Space.parse(raw)
print(space.surface_area())
print(space.external_surface_area())
