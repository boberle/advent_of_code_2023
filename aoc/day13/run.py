from dataclasses import dataclass
from pathlib import Path


@dataclass
class Point:
    x: int
    y: int


@dataclass
class Board:
    width: int
    height: int
    points: list[Point]

    def find_mirror_column(self, smudge_count: int) -> int | None:
        points = {(p.x, p.y) for p in self.points}
        for col in range(1, self.width):
            smudges = 0
            for x, y in points:
                expected = col - x + col - 1
                if not (0 <= expected <= self.width - 1):
                    continue
                if (expected, y) not in points:
                    smudges += 1
            if smudges == smudge_count:
                return col
        return None

    def find_mirror_row(self, smudge_count: int) -> int | None:
        points = {(p.x, p.y) for p in self.points}
        for row in range(1, self.height):
            smudges = 0
            for x, y in points:
                expected = row - y + row - 1
                if not (0 <= expected <= self.height - 1):
                    continue
                if (x, expected) not in points:
                    smudges += 1
            if smudges == smudge_count:
                return row
        return None


def run(file: Path) -> None:
    boards = parse(file)
    print(compute_summary(boards, 0))
    print(compute_summary(boards, 1))


def compute_summary(boards: list[Board], smudge_count: int) -> int:
    total_col = 0
    total_row = 0
    for board in boards:
        col = board.find_mirror_column(smudge_count)
        if col is not None:
            total_col += col
            continue
        row = board.find_mirror_row(smudge_count)
        assert row is not None
        total_row += row
    return total_col + 100 * total_row


def parse(file: Path) -> list[Board]:
    rv = []
    points: list[Point] = []
    width = 0
    height = 0
    for line in file.open():
        line = line.strip()
        if not line:
            rv.append(Board(width, height, points))
            width = 0
            height = 0
            points = []
            continue
        if height == 0:
            width = len(line)
        for i, c in enumerate(line):
            if c == "#":
                points.append(Point(i, height))
        height += 1

    rv.append(Board(width, height, points))
    return rv
