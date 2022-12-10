from functools import cached_property
from pathlib import Path
from dataclasses import dataclass
from typing import Literal

file = Path(__file__).parent.parent / "data" / "day10.txt"
raw = file.read_text().strip()


@dataclass
class NoopInstruction:
    code: Literal['noop'] = 'noop'


@dataclass
class AddxInstruction:
    value: int
    code: Literal['addx'] = 'addx'


@dataclass
class Cpu:
    data: str

    @property
    def instructions(self):
        for line in self.data.splitlines():
            match line.split():
                case [NoopInstruction.code]:
                    yield NoopInstruction()
                case [AddxInstruction.code, x]:
                    yield AddxInstruction(value=int(x))

    @cached_property
    def values(self):
        values = [1]
        for instr in self.instructions:
            values.append(values[-1])
            if instr.code == AddxInstruction.code:
                values.append(values[-1] + instr.value)
        return values

    def signal_strength(self, cycle: int):
        return self.values[cycle-1] * cycle

    def get_signal_strengths(self):
        return sum(self.signal_strength(i) for i in range(20, 221, 40))

    def draw(self):
        output = []
        row = []
        for i, val in enumerate(self.values):
            x = i % 40
            cycle = x + 1
            if x == 0 and row:
                output.append(row)
                row = []
            row.append('#' if cycle in range(val, val + 3) else '.')
        return '\n'.join(''.join(row) for row in output)


cpu = Cpu(raw)
value = cpu.get_signal_strengths()
print(value)

drawing = cpu.draw()
print(drawing)
