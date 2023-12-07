from collections import Counter
from dataclasses import dataclass
from enum import Enum, auto
from functools import cached_property
from pathlib import Path


class CardLabel(int, Enum):
    CJ = auto()  # the J for the second part
    C2 = auto()
    C3 = auto()
    C4 = auto()
    C5 = auto()
    C6 = auto()
    C7 = auto()
    C8 = auto()
    C9 = auto()
    T = auto()
    J = auto()  # the J for the first part
    Q = auto()
    K = auto()
    A = auto()


class CardType(int, Enum):
    HighCard = auto()
    OnePair = auto()
    TwoPair = auto()
    ThreeKind = auto()
    FullHouse = auto()
    FourKind = auto()
    FiveKind = auto()


@dataclass
class Hand:
    cards: list[CardLabel]

    @cached_property
    def type(self) -> CardType:
        counter = Counter(self.cards)
        if 5 in counter.values():
            return CardType.FiveKind
        if 4 in counter.values():
            return CardType.FourKind
        if 3 in counter.values() and 2 in counter.values():
            return CardType.FullHouse
        if 3 in counter.values():
            return CardType.ThreeKind
        if list(counter.values()).count(2) == 2:
            return CardType.TwoPair
        if 2 in counter.values():
            return CardType.OnePair
        return CardType.HighCard

    def __lt__(self, other: "Hand") -> bool:
        if self.type == other.type:
            for a, b in zip(self.cards, other.cards):
                if a == b:
                    continue
                else:
                    return a < b
            return False
        else:
            return self.type < other.type

    @staticmethod
    def from_string(s: str) -> "Hand":
        assert len(s) == 5
        cards: list[CardLabel] = []
        for c in s:
            if c.isdigit():
                cards.append(CardLabel[f"C{c}"])
            else:
                cards.append(CardLabel[c])
        return Hand(cards)


class Part2Hand(Hand):
    @cached_property
    def type(self) -> CardType:
        counter = Counter(self.cards)
        assert CardLabel.J not in counter
        if len(counter) > 1 and CardLabel.CJ in counter:
            del counter[CardLabel.CJ]
            most = counter.most_common(1)[0][0]
            cards = [most if l == CardLabel.CJ else l for l in self.cards]
            card = Hand(cards=cards)
            return card.type
        else:
            return super().type

    @staticmethod
    def from_hand(hand: Hand) -> "Part2Hand":
        cards = [CardLabel.CJ if l == CardLabel.J else l for l in hand.cards]
        return Part2Hand(cards=list(cards))


@dataclass
class Bid:
    hand: Hand
    bid: int


def run(file: Path) -> None:
    bids = parse(file)
    print(compute_winnings(bids))

    bids = [
        Bid(
            hand=Part2Hand.from_hand(b.hand),
            bid=b.bid,
        )
        for b in bids
    ]
    print(compute_winnings(bids))


def parse(file: Path) -> list[Bid]:
    rv = []
    for line in file.open():
        hand, bid = line.strip().split()
        rv.append(
            Bid(
                hand=Hand.from_string(hand),
                bid=int(bid),
            )
        )
    return rv


def compute_winnings(bids: list[Bid]) -> int:
    bids.sort(key=lambda b: b.hand)
    total = 0
    for i, bid in enumerate(bids):
        total += (i + 1) * bid.bid
    return total
