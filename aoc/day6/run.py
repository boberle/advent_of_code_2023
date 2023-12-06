import re
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Race:
    time: int
    distance: int


def run(file: Path) -> None:
    races = parse(file)
    print(compute_possibilities(races))
    # print(compute_possibilities([merge_races(races)]))
    print(compute_possibilities_for_one_race(merge_races(races)))


def compute_possibilities(races: list[Race]) -> int:
    total = 1
    for race in races:
        count = 0
        for i in range(1, race.time):
            if (race.time - i) * i > race.distance:
                count += 1
        total *= count
    return total


def parse(file: Path) -> list[Race]:
    lines = file.read_text().splitlines(keepends=False)
    m1 = re.findall(r"\d+", lines[0])
    m2 = re.findall(r"\d+", lines[1])
    return [Race(int(t), int(d)) for t, d in zip(m1, m2)]


def merge_races(races: list[Race]) -> Race:
    return Race(
        time=int("".join(str(r.time) for r in races)),
        distance=int("".join(str(r.distance) for r in races)),
    )


def compute_possibilities_for_one_race(race: Race) -> int:
    a = 0
    while a < race.time and (race.time - a) * a < race.distance:
        a += 1

    b = race.time
    while b <= race.time and (race.time - b) * b < race.distance:
        b -= 1

    return race.time - a - (race.time - b) + 1
