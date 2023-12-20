from collections import defaultdict
from dataclasses import dataclass
from enum import Enum, auto
from pathlib import Path
from typing import Generator


class Rock(int, Enum):
    Empty = auto()
    Cube = auto()
    Round = auto()


@dataclass
class Board:
    width: int
    height: int
    mat: list[list[Rock]]

    def get_col(self, index: int) -> Generator[tuple[int, Rock], None, None]:
        for i, row in enumerate(self.mat):
            if row[index] != Rock.Empty:
                yield i, row[index]

    def get_rcol(self, index: int) -> Generator[tuple[int, Rock], None, None]:
        for i in range(self.height):
            pos = self.height - i - 1
            if self.mat[pos][index] != Rock.Empty:
                yield pos, self.mat[pos][index]

    def get_row(self, index: int) -> Generator[tuple[int, Rock], None, None]:
        for i, c in enumerate(self.mat[index]):
            if c != Rock.Empty:
                yield i, c

    def get_rrow(self, index: int) -> Generator[tuple[int, Rock], None, None]:
        for i in range(self.width):
            pos = self.width - i - 1
            if self.mat[index][pos] != Rock.Empty:
                yield pos, self.mat[index][pos]

    def move(self, src: tuple[int, int], target: tuple[int, int]) -> None:
        self.mat[src[1]][src[0]] = Rock.Empty
        self.mat[target[1]][target[0]] = Rock.Round

    def tilt_north(self) -> None:
        for col in range(self.width):
            cur = 0
            for pos, type in self.get_col(col):
                if pos == cur:
                    cur += 1
                elif cur < pos and type == Rock.Round:
                    self.move((col, pos), (col, cur))
                    cur += 1
                elif type == Rock.Cube:
                    cur = pos + 1

    def tilt_south(self) -> None:
        for col in range(self.width):
            cur = self.height - 1
            for pos, type in self.get_rcol(col):
                if pos == cur:
                    cur -= 1
                elif cur > pos and type == Rock.Round:
                    self.move((col, pos), (col, cur))
                    cur -= 1
                elif type == Rock.Cube:
                    cur = pos - 1

    def tilt_west(self) -> None:
        for row in range(self.height):
            cur = 0
            for pos, type in self.get_row(row):
                if pos == cur:
                    cur += 1
                elif cur < pos and type == Rock.Round:
                    self.move((pos, row), (cur, row))
                    cur += 1
                elif type == Rock.Cube:
                    cur = pos + 1

    def tilt_east(self) -> None:
        for row in range(self.height):
            cur = self.width - 1
            for pos, type in self.get_rrow(row):
                if pos == cur:
                    cur -= 1
                elif cur > pos and type == Rock.Round:
                    self.move((pos, row), (cur, row))
                    cur -= 1
                elif type == Rock.Cube:
                    cur = pos - 1

    def compute_load(self) -> int:
        total = 0
        for i, row in enumerate(self.mat):
            for rock in row:
                if rock == Rock.Round:
                    total += self.height - i
        return total

    def print(self) -> None:
        mapping = {
            Rock.Empty: ".",
            Rock.Cube: "#",
            Rock.Round: "O",
        }
        for row in self.mat:
            print("".join(mapping[r] for r in row))


def run(file: Path) -> None:
    board = parse(file)
    board.tilt_north()
    print(board.compute_load())

    board = parse(file)
    loads: dict[int, list[int]] = defaultdict(list)
    for i in range(1, 100000):
        cycle(board)
        load = board.compute_load()
        loads[load].append(i)

        if (data := is_sequence(loads[load])) is not None:
            init, diff = data
            if (1000000000 - init) % diff == 0:
                print(load)
                break


def is_sequence(seq: list[int]) -> tuple[int, int] | None:
    if len(seq) < 4:
        return None
    diff = seq[1] - seq[0]
    for i in range(2, len(seq)):
        if seq[i] - seq[i - 1] != diff:
            return None
    return seq[0], diff


def cycle(board: Board) -> None:
    board.tilt_north()
    board.tilt_west()
    board.tilt_south()
    board.tilt_east()


def parse(file: Path) -> Board:
    width = 0
    height = 0
    mat = []
    for line in file.open():
        line = line.strip()
        if height == 0:
            width = len(line)
        row: list[Rock] = []
        mat.append(row)
        for i, c in enumerate(line):
            if c == "O":
                row.append(Rock.Round)
            elif c == "#":
                row.append(Rock.Cube)
            else:
                row.append(Rock.Empty)
        height += 1
    return Board(width, height, mat)
