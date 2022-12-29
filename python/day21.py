from pathlib import Path
from dataclasses import dataclass, field
import re
from sympy import Symbol, solve
import operator

file = Path(__file__).parent.parent / "data" / "day21.txt"
raw = file.read_text().strip()


@dataclass
class Monkey:
    name: str
    expr: str


@dataclass
class MonkeyGroup:
    monkeys: dict[str, Monkey]
    cache: dict[str, int] = field(default_factory=dict)
    expand_cache: dict = field(default_factory=lambda: {'humn': Symbol('humn')})

    def evaluate(self, monkey: str):
        if monkey in self.cache:
            return self.cache[monkey]
        m = self.monkeys[monkey]
        if m.expr.isdigit():
            ret = int(m.expr)
            self.cache[monkey] = ret
        else:
            m1, m2 = re.split(r' [\+\-\*\/] ', m.expr)
            m1val = self.evaluate(m1)
            m2val = self.evaluate(m2)
            expr = m.expr.replace(m1, str(m1val))
            expr = expr.replace(m2, str(m2val))
            ret: int = int(eval(expr))
            self.cache[monkey] = ret
        return ret

    def expand(self, monkey: str):
        if monkey in self.expand_cache:
            return self.expand_cache[monkey]
        expr = self.monkeys[monkey].expr
        if expr.isdigit():
            return int(expr)
        else:
            m1, m2 = re.split(r' [\+\-\*\/\=] ', expr)
            action = re.search(r'([\+\-\*\/\=])', expr)
            assert action
            m1val = self.expand(m1)
            m2val = self.expand(m2)
            matches = {
                '+': operator.add,
                '-': operator.sub,
                '/': operator.truediv,
                '*': operator.mul,
            }
            ret = matches[action.group(0)](m1val, m2val)
            self.expand_cache[monkey] = ret
            return ret


def get_monkeys(data: str):
    monkeys: dict[str, Monkey] = {}
    for line in data.splitlines():
        monkey, expr = line.split(':')
        expr = expr.strip()
        monkeys[monkey] = Monkey(monkey, expr)
    mg = MonkeyGroup(monkeys)
    return mg


def part1():
    group = get_monkeys(raw)
    root_val = group.evaluate('root')
    return root_val

def part2():
    group = get_monkeys(raw)
    root = group.monkeys['root']
    root.expr = root.expr.replace('+', '-')
    root_val = group.expand('root')
    value = int(solve(root_val, group.expand_cache['humn'])[0])
    return value

print(f'{part1()=}')
print(f'{part2()=}')
