import re
from dataclasses import dataclass
from functools import cached_property
from pathlib import Path


@dataclass
class Card:
    id: int
    winning: list[int]
    you_have: list[int]

    @cached_property
    def matching_numbers(self) -> int:
        count = 0
        for n in self.you_have:
            if n in self.winning:
                count += 1
        return count


def run(file: Path) -> None:
    cards = parse(file)

    total = 0
    for card in cards:
        if card.matching_numbers:
            total += 2 ** (card.matching_numbers - 1)
    print(total)

    print(compute_total_cards(cards))


def parse(file: Path) -> list[Card]:
    rv = []
    for line in file.open():
        m = re.fullmatch(r"Card +(\d+):((?: +\d+)+) +\|((?: +\d+)*)", line.strip())
        assert m
        rv.append(
            Card(
                id=int(m.group(1)),
                winning=list(map(int, m.group(2).split())),
                you_have=list(map(int, m.group(3).split())),
            )
        )
    return rv


def compute_total_cards(cards: list[Card]) -> int:
    totals = [1] * len(cards)
    for c, card in enumerate(cards):
        for i in range(c + 1, c + 1 + card.matching_numbers):
            totals[i] += totals[c]
    return sum(totals)
