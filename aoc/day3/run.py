import re
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Number:
    value: int
    x1: int
    x2: int
    y: int


@dataclass
class Symbol:
    value: str
    x: int
    y: int


@dataclass
class Gear:
    n1: Number
    n2: Number


def run(file: Path) -> None:
    numbers, symbols = parse(file)
    part_numbers = find_part_numbers(numbers, symbols)
    print(sum([n.value for n in part_numbers]))

    gears = find_gears(part_numbers, symbols)
    total = 0
    for gear in gears:
        total += gear.n1.value * gear.n2.value
    print(total)


def parse(file: Path) -> tuple[list[Number], list[Symbol]]:
    nums = []
    syms = []
    for i, line in enumerate(file.open()):
        pos = 0
        for m in re.finditer(r"(\d+|\.|.)", line):
            v = m.group(0)
            if v == ".":
                pos += 1
            elif v.isdigit():
                nums.append(Number(int(v), pos, pos + len(v) - 1, i))
                pos += len(v)
            else:
                syms.append(Symbol(v, pos, i))
                pos += 1
    return nums, syms


def find_part_numbers(numbers: list[Number], symbols: list[Symbol]) -> list[Number]:
    parts = []
    for number in numbers:
        for symbol in symbols:
            if (
                number.x1 - 1 <= symbol.x <= number.x2 + 1
                and number.y - 1 <= symbol.y <= number.y + 1
            ):
                parts.append(number)
                break
    return parts


def find_gears(numbers: list[Number], symbols: list[Symbol]) -> list[Gear]:
    gears = []
    for symbol in symbols:
        if symbol.value != "*":
            continue
        nums = []
        for number in numbers:
            if (
                number.x1 - 1 <= symbol.x <= number.x2 + 1
                and number.y - 1 <= symbol.y <= number.y + 1
            ):
                nums.append(number)
        if len(nums) == 2:
            gears.append(Gear(*nums))
    return gears
