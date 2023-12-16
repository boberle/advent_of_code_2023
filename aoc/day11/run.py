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
    galaxies: list[Point]

    def expand(self, n: int) -> None:
        columns_to_expand = []
        for x in range(self.width):
            for galaxy in self.galaxies:
                if galaxy.x == x:
                    break
            else:
                columns_to_expand.append(x)
        for i, x in enumerate(columns_to_expand):
            x += i * n
            for galaxy in self.galaxies:
                if galaxy.x > x:
                    galaxy.x += n

        rows_to_expand = []
        for y in range(self.height):
            for galaxy in self.galaxies:
                if galaxy.y == y:
                    break
            else:
                rows_to_expand.append(y)
        for i, y in enumerate(rows_to_expand):
            y += i * n
            for galaxy in self.galaxies:
                if galaxy.y > y:
                    galaxy.y += n

    def compute_sum_of_shortest_paths(self) -> int:
        total = 0
        for g in self.galaxies:
            for h in self.galaxies:
                if g == h:
                    continue
                total += abs(g.x - h.x) + abs(g.y - h.y)
        return total


def run(file: Path) -> None:
    board = parse(file)
    board.expand(1)
    print(board.compute_sum_of_shortest_paths() / 2)

    board = parse(file)
    board.expand(1000000 - 1)
    print(board.compute_sum_of_shortest_paths() / 2)


def parse(file: Path) -> Board:
    width = 0
    height = 0
    points = []
    for y, line in enumerate(file.open()):
        for x, c in enumerate(line.strip()):
            if y == 0:
                width += 1
            if c == "#":
                points.append(Point(x, y))
        height += 1
    return Board(width, height, points)
