from pathlib import Path

file = Path(__file__).parent.parent / "data" / "day25.txt"
raw = file.read_text()

class Snafu:
    def __init__(self, value: str|list[str]) -> None:
        self.value = self.parse(value)

    def parse(self, value: str|list[str]) -> int:
        total = 0
        for i, digit in enumerate(reversed(value)):
            match digit:
                case '=':
                    n = -2
                case '-':
                    n = -1
                case x:
                    n = int(x)
            total += (n * (5**i))
        return total

    @staticmethod
    def subtract_1(n: str):
        convert = {
            '-': '=',
            '0': '-',
            '1': '0',
            '2': '1',
        }
        return convert.get(n, None)

    def __repr__(self):
        return f'{self.value}'

    @classmethod
    def find(cls, val: int):
        digits = ['2']
        while True:
            digits.append('2')
            n = cls(digits)
            if n.value > val:
                digits2 = digits[:]
                digits2[0] = '1'
                n = cls(digits2)
                if n.value > val:
                    digits = digits2
                elif n.value == val:
                    return cls(digits)
                break
        for i in range(1, len(digits)):
            while change := cls.subtract_1(digits[i]):
                old_val = digits[i]
                digits[i] = change
                n = cls(digits)
                if n.value == val:
                    return ''.join(digits)
                elif n.value < val:
                    digits[i] = old_val
                    break


def get_nums(data: str):
    nums: list[Snafu] = []
    for line in data.splitlines():
        n = Snafu(line)
        nums.append(n)
    return nums

def part1():
    nums = get_nums(raw)
    out = sum(x.value for x in nums)
    x = Snafu.find(out)
    return x

print(f'{part1()=}')
