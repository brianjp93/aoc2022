from functools import cached_property
from pathlib import Path
from dataclasses import dataclass
from math import lcm, prod

file = Path(__file__).parent.parent / "data" / "day11.txt"
raw = file.read_text().strip()


@dataclass
class Monkey:
    items: list[int]
    operation: str
    test: int
    if_true: int
    if_false: int
    inspection_count = 0

    @classmethod
    def parse(cls, data: str):
        _, a, b, c, d, e = data.splitlines()
        items = list(map(int, a.split(':')[1].split(',')))
        operation = b.split('=')[1].strip()
        operation = '{old}'.join(operation.split('old'))
        test = int(c.split()[-1])
        if_true = int(d.split()[-1])
        if_false = int(e.split()[-1])
        return cls(items=items, operation=operation, test=test, if_true=if_true, if_false=if_false)

    def throw_to(self, item_id: int, maximum_worry=False, divisor=0):
        self.inspection_count += 1
        item = self.items[item_id]
        val: int = eval(self.operation.format(old=item))
        if not maximum_worry:
            val = val // 3
        if divisor:
            val = val % divisor
        self.items[item_id] = val
        is_pass = val % self.test == 0
        return self.if_true if is_pass else self.if_false


@dataclass
class MonkeyList:
    monkeys: list[Monkey]
    maximum_worry = False

    def do_round(self):
        for monkey in self.monkeys:
            self.do_turn(monkey)

    def do_turn(self, monkey: Monkey):
        for i in range(len(monkey.items)):
            throw_to = monkey.throw_to(i, maximum_worry=self.maximum_worry, divisor=self.lcm)
            self.monkeys[throw_to].items.append(monkey.items[i])
        monkey.items = []

    @cached_property
    def lcm(self):
        return lcm(*(x.test for x in self.monkeys))


def get_monkeys():
    return MonkeyList(monkeys=[Monkey.parse(x) for x in raw.split('\n\n')])


if __name__ == '__main__':
    monkeys = get_monkeys()
    for i in range(20):
        monkeys.do_round()

    out = sorted((x.inspection_count for x in monkeys.monkeys))
    print(prod(out[-2:]))

    monkeys = get_monkeys()
    monkeys.maximum_worry = True
    for i in range(10_000):
        monkeys.do_round()
    out = sorted((x.inspection_count for x in monkeys.monkeys))
    print(prod(out[-2:]))
