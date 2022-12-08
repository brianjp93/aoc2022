from dataclasses import dataclass
from functools import cached_property
from pathlib import Path
from typing import Self

file = Path(__file__).parent.parent / "data" / "day8.txt"
raw = file.read_text().strip()


@dataclass
class Tree:
    value: int
    up: Self | None = None
    down: Self | None = None
    left: Self | None = None
    right: Self | None = None

    def __repr__(self):
        return f"{self.value}"

    @cached_property
    def surroundings(self):
        dirs: dict[str, list[Tree]] = {
            "up": [],
            "down": [],
            "left": [],
            "right": [],
        }
        for direction in dirs.keys():
            node: Tree = self
            while node := getattr(node, direction):
                dirs[direction].append(node)
        return dirs

    def is_visible(self):
        for items in self.surroundings.values():
            if len([x for x in items if x.value >= self.value]) == 0:
                return True
        return False

    def score(self):
        score = 1
        for trees in self.surroundings.values():
            if not trees:
                return 0
            i = None
            found = False
            for i, tree in enumerate(trees, 1):
                if tree.value >= self.value:
                    score *= i
                    found = True
                    break
            if not found and i:
                score *= i
        return score


class Forest:
    def __init__(self, data: str):
        self.map = self.parse(data)

    def parse(self, data: str):
        m: dict[tuple[int, int], Tree] = {}
        for y, row in enumerate(data.splitlines()):
            for x, ch in enumerate(row):
                m[(x, y)] = Tree(value=int(ch))

        for (x, y), tree in m.items():
            tree.left = m.get((x - 1, y))
            tree.right = m.get((x + 1, y))
            tree.up = m.get((x, y - 1))
            tree.down = m.get((x, y + 1))
        return m

    def count_visible(self):
        return sum(x.is_visible() for x in self.map.values())

    def scenic_scores(self):
        return [x.score() for x in self.map.values() if x.is_visible()]


if __name__ == "__main__":
    forest = Forest(raw)
    print(forest.count_visible())
    print(max(forest.scenic_scores()))
