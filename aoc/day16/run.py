from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto
from pathlib import Path


class ElementType(int, Enum):
    VS = auto()  # vertical splitter |
    HS = auto()  # horizontal splitter -
    RM = auto()  # right mirror /
    LM = auto()  # left mirror \


@dataclass
class Point:
    x: int
    y: int

    def __hash__(self) -> int:
        return hash((self.x, self.y))


@dataclass
class OrientedPoint:
    x: int
    y: int
    direction: Direction

    def __hash__(self) -> int:
        return hash((self.x, self.y, self.direction))


@dataclass
class Board:
    width: int
    height: int
    elements: dict[Point, ElementType]


class Direction(int, Enum):
    North = auto()
    East = auto()
    South = auto()
    West = auto()


class Dead(Exception):
    ...


@dataclass
class Beam:
    position: Point
    direction: Direction
    visited: set[OrientedPoint] = field(default_factory=set)

    def move(self, board: Board) -> Beam | None:
        op = OrientedPoint(self.position.x, self.position.y, self.direction)
        if op in self.visited:
            raise Dead
        self.visited.add(op)

        pos: Point
        match self.direction:
            case Direction.East:
                pos = Point(self.position.x + 1, self.position.y)
            case Direction.West:
                pos = Point(self.position.x - 1, self.position.y)
            case Direction.North:
                pos = Point(self.position.x, self.position.y - 1)
            case Direction.South:
                pos = Point(self.position.x, self.position.y + 1)
            case _:
                assert False

        self.position = pos

        if not (0 <= pos.x < board.width) or not (0 <= pos.y < board.height):
            raise Dead

        if pos not in board.elements:
            return None

        match board.elements[pos]:
            case ElementType.VS:
                if self.direction in (Direction.East, Direction.West):
                    self.direction = Direction.South
                    if pos.y > 0:
                        return Beam(pos, Direction.North, self.visited)
            case ElementType.HS:
                if self.direction in (Direction.North, Direction.South):
                    self.direction = Direction.East
                    if pos.x > 0:
                        return Beam(pos, Direction.West, self.visited)
            case ElementType.RM:  # /
                match self.direction:
                    case Direction.North:
                        self.direction = Direction.East
                    case Direction.East:
                        self.direction = Direction.North
                    case Direction.South:
                        self.direction = Direction.West
                    case Direction.West:
                        self.direction = Direction.South
                    case _:
                        assert False
            case ElementType.LM:  # \
                match self.direction:
                    case Direction.North:
                        self.direction = Direction.West
                    case Direction.East:
                        self.direction = Direction.South
                    case Direction.South:
                        self.direction = Direction.East
                    case Direction.West:
                        self.direction = Direction.North
                    case _:
                        assert False
            case _:
                assert False

        return None

    def __hash__(self) -> int:
        return hash(id(self))


def run(file: Path) -> None:
    board = parse(file)

    initial = Beam(Point(-1, 0), Direction.East)
    print(get_energized(board, initial))

    max_ = 0
    for x in range(board.width):
        initial = Beam(Point(x, -1), Direction.South)
        max_ = max(max_, get_energized(board, initial))
        initial = Beam(Point(x, board.height), Direction.North)
        max_ = max(max_, get_energized(board, initial))
    for y in range(board.height):
        initial = Beam(Point(-1, y), Direction.East)
        max_ = max(max_, get_energized(board, initial))
        initial = Beam(Point(board.width, y), Direction.West)
        max_ = max(max_, get_energized(board, initial))
    print(max_)


def get_energized(board: Board, initial: Beam) -> int:
    beams: set[Beam] = {initial}
    energized: set[Point] = set()

    while beams:
        removed: set[Beam] = set()
        added: set[Beam] = set()
        for beam in beams:
            if (
                0 <= beam.position.x < board.width
                and 0 <= beam.position.y < board.height
            ):
                energized.add(beam.position)
            try:
                other_beam = beam.move(board)
            except Dead:
                removed.add(beam)
            else:
                if other_beam:
                    added.add(other_beam)
        for beam in removed:
            beams.remove(beam)
        for beam in added:
            beams.add(beam)

    return len(energized)


def parse(file: Path) -> Board:
    mapping = {
        "|": ElementType.VS,
        "-": ElementType.HS,
        "/": ElementType.RM,
        "\\": ElementType.LM,
    }
    width = 0
    height = 0
    elements: dict[Point, ElementType] = dict()
    for line in file.open():
        line = line.strip()
        width = len(line)
        for i, c in enumerate(line):
            if c in mapping:
                elements[Point(i, height)] = mapping[c]
        height += 1
    return Board(width, height, elements)
