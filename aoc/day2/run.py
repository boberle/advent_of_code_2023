import re
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Subset:
    green: int = 0
    blue: int = 0
    red: int = 0


@dataclass
class Game:
    id: int
    subsets: list[Subset]


def run(file: Path) -> None:
    games = parse(file)
    impossible, possible = partition(games)
    print(sum(game.id for game in impossible))

    print(sum(compute_power(game) for game in games))


def parse(file: Path) -> list[Game]:
    rv = []
    for line in file.open():
        rv.append(parse_game(line))
    return rv


def parse_game(line: str) -> Game:
    pos = 0
    game_id = None
    subsets: list[Subset] = []
    current: Subset = Subset()
    while pos < len(line) - 1:
        if m := re.match(r"Game (\d+): ", line[pos:]):
            assert game_id is None
            game_id = int(m.group(1))
        elif m := re.match(r"(\d+) blue", line[pos:]):
            current.blue = int(m.group(1))
        elif m := re.match(r"(\d+) red", line[pos:]):
            current.red = int(m.group(1))
        elif m := re.match(r"(\d+) green", line[pos:]):
            current.green = int(m.group(1))
        elif m := re.match(r", ", line[pos:]):
            ...
        elif m := re.match(r"; ", line[pos:]):
            subsets.append(current)
            current = Subset()
        else:
            assert False
        pos += len(m.group(0))
    subsets.append(current)
    assert game_id is not None
    return Game(game_id, subsets)


def partition(games: list[Game]) -> tuple[list[Game], list[Game]]:
    possible = []
    impossible = []
    for game in games:
        p = True
        for subset in game.subsets:
            if subset.red > 12 or subset.green > 13 or subset.blue > 14:
                p = False
                break
        if p:
            possible.append(game)
        else:
            impossible.append(game)
    return possible, impossible


def compute_power(game: Game) -> int:
    min_set = Subset()
    for subset in game.subsets:
        min_set.red = max(min_set.red, subset.red)
        min_set.green = max(min_set.green, subset.green)
        min_set.blue = max(min_set.blue, subset.blue)
    return min_set.red * min_set.green * min_set.blue
