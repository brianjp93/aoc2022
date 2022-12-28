from pathlib import Path
from dataclasses import dataclass
from typing import Self

file = Path(__file__).parent.parent / "data" / "day20.txt"
raw = file.read_text().strip()


@dataclass
class Link:
    value: int
    _prev: None | Self = None
    _next: None | Self = None

    @property
    def prev(self):
        return self._prev

    @prev.setter
    def prev(self, other: Self):
        self._prev = other
        other._next = self

    @property
    def next(self):
        return self._next

    @next.setter
    def next(self, other: Self):
        self._next = other
        other._prev = self

    def pop(self):
        assert self.prev and self.next
        self.prev.next = self.next
        self._prev = self._next = None

    def push(self, other: Self):
        assert self.next
        other.next = self.next
        self.next = other

    def current_order(self):
        out = [self]
        node = self.next
        while node is not self:
            assert node
            out.append(node)
            node = node.next
        return out

    def print(self):
        print(str([x.value for x in self.current_order()]))

    def get_link(self, val: int):
        assert val >= 0
        node = self
        for _ in range(val):
            node = node.next
            assert node
        return node

    def move(self, val: int, length: int):
        if val == 0:
            return
        val = val % (length - 1)
        link = self.get_link(val)
        if link == self:
            return
        assert link.next
        self.pop()
        link.push(self)

    def mix(self, count=1):
        order = self.current_order()
        length = len(order)
        for _ in range(count):
            for link in order:
                link.move(link.value, length)

    def find(self, val: int):
        node = self.next
        while node and node is not self and node.value != val:
            node = node.next
        assert node
        return node

    def grove_coordinates(self):
        zero = self.find(0)
        length = len(self.current_order())
        _1000 = 1000 % length
        _2000 = 2000 % length
        _3000 = 3000 % length
        values = [zero.get_link(i).value for i in [_1000, _2000, _3000]]
        return sum(values)


def get_root(data: str, encryption_key=1):
    values = [int(x) * encryption_key for x in data.splitlines()]
    root = Link(value=values[0])
    node = root
    link = None
    for value in values[1:]:
        link = Link(value=value)
        node.next = link
        node = link
    if link:
        link.next = root
    return root


root = get_root(raw)
node = root
root.mix()
print(root.grove_coordinates())

KEY = 811589153
root = get_root(raw, encryption_key=KEY)
root.mix(10)
print(root.grove_coordinates())
