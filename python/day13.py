from math import prod
from functools import cmp_to_key
from pathlib import Path
from ast import literal_eval
from typing import TypeAlias

file = Path(__file__).parent.parent / "data" / "day13.txt"
raw = file.read_text().strip()

ListPiece: TypeAlias = int | list['ListPiece']

LESSER = -1
EQUAL = 0
GREATER = 1

def parse(data: str) -> list[tuple[ListPiece, ListPiece]]:
    return [tuple(map(literal_eval, pair.split('\n'))) for pair in data.split('\n\n')]

def compare(a: ListPiece, b: ListPiece):
    match [a, b]:
        case [list() as a, list() as b]:
            for c, d in zip(a, b):
                result = compare(c, d)
                if result != EQUAL:
                    return result
            if len(a) < len(b):
                return LESSER
            elif len(a) > len(b):
                return GREATER
            return EQUAL
        case [int() as a, int() as b]:
            if a < b:
                return LESSER
            elif a == b:
                return EQUAL
            else:
                return GREATER
        case [list() as a, int() as b]:
            return compare(a, [b])
        case [int() as a, list() as b]:
            return compare([a], b)
    raise Exception('how did we get here.')


pairs = parse(raw)
print(f'Part 1: {sum([i+1 for i, pair in enumerate(pairs) if compare(*pair) == LESSER])}')

DECODER_KEYS: ListPiece = [[[2]], [[6]]]
complete_list = sum([list(pair) for pair in pairs], start=[]) + DECODER_KEYS
complete_list.sort(key=cmp_to_key(compare))
p2 = prod([i+1 for i, x in enumerate(complete_list) if x in DECODER_KEYS])
print(f'Part 2: {p2}')
