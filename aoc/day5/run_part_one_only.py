import re
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Seed:
    id: int


@dataclass
class Range:
    target: int
    source: int
    length: int

    def convert(self, value: int) -> int | None:
        if self.source <= value <= self.source + self.length:
            return self.target + (value - self.source)
        return None


@dataclass
class Mapping:
    source_cat: str
    target_cat: str
    ranges: list[Range] = field(default_factory=list)

    def convert(self, value: int) -> int:
        for range in self.ranges:
            if (rv := range.convert(value)) is not None:
                return rv
        return value


@dataclass
class MappingSet:
    mappings: dict[str, Mapping] = field(default_factory=dict)

    def convert(self, value: int, source: str) -> int:
        return self.mappings[source].convert(value)

    def convert_seed_to_location(self, value: int) -> int:
        source = "seed"
        while source != "location":
            value = self.mappings[source].convert(value)
            source = self.mappings[source].target_cat
        return value


def run(file: Path) -> None:
    mappings, seeds = parse(file)
    print(min(mappings.convert_seed_to_location(seed.id) for seed in seeds))


def parse(file: Path) -> tuple[MappingSet, list[Seed]]:
    seeds: list[Seed] = []
    mapping_set = MappingSet()
    current_mapping = None

    for line in file.open():
        line = line.strip()
        if m := re.match(r"seeds:((?: \d+)+)", line):
            seeds = [Seed(id=int(v)) for v in m.group(1).split()]
        elif m := re.fullmatch(r"([a-z]+)-to-([a-z]+) map:", line):
            if current_mapping is not None:
                mapping_set.mappings[current_mapping.source_cat] = current_mapping
            current_mapping = Mapping(
                source_cat=m.group(1),
                target_cat=m.group(2),
            )
        elif len(line) > 0:
            assert current_mapping is not None, line
            current_mapping.ranges.append(Range(*list(map(int, line.split()))))
        elif len(line) == 0:
            ...
        else:
            assert False, line

    if current_mapping is not None:
        mapping_set.mappings[current_mapping.source_cat] = current_mapping

    assert seeds
    return mapping_set, seeds
