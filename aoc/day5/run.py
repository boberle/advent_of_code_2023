import re
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Range:
    start: int
    end: int
    transformed: bool = False


@dataclass
class Transformation:
    start: int
    end: int
    shift: int

    def apply(self, range: Range) -> list["Range"]:
        # case 2 and 3: dissociation
        if range.end < self.start or self.end < range.start:
            return [Range(range.start, range.end)]
        # case 4 and 5: partial overlap, with external elements
        if range.start < self.start and range.end <= self.end:
            return [
                Range(range.start, self.start - 1),
                Range(
                    self.start + self.shift, range.end + self.shift, transformed=True
                ),
            ]
        if self.start <= range.start and self.end < range.end:
            return [
                Range(
                    range.start + self.shift, self.end + self.shift, transformed=True
                ),
                Range(self.end + 1, range.end),
            ]
        # case 1 (equality) or case 6: partial overlap, no external elements
        if self.start <= range.start and range.end <= self.end:
            return [
                Range(
                    range.start + self.shift, range.end + self.shift, transformed=True
                )
            ]
        # case 7: total overlap + external elements
        if range.start < self.start and self.end < range.end:
            return [
                Range(range.start, self.start - 1),
                Range(self.start + self.shift, self.end + self.shift, transformed=True),
                Range(self.end + 1, range.end),
            ]
        assert False, (range, self)


@dataclass
class Mapping:
    source: str
    target: str
    transformations: list[Transformation] = field(default_factory=list)

    def convert(self, range: Range) -> list[Range]:
        ranges = [range]
        for trans in self.transformations:
            new_ranges = []
            for range in ranges:
                if range.transformed:
                    new_ranges.append(range)
                else:
                    new_ranges.extend(trans.apply(range))
            ranges = new_ranges
        for range in ranges:
            range.transformed = False
        return ranges


@dataclass
class MappingSet:
    mappings: dict[str, Mapping] = field(default_factory=dict)

    def convert_seed_to_location(self, ranges: list[Range]) -> list[Range]:
        source = "seed"
        while source != "location":
            new_ranges = []
            for range in ranges:
                foo = self.mappings[source].convert(range)
                new_ranges.extend(foo)
            ranges = new_ranges
            source = self.mappings[source].target
        return ranges


def run(file: Path) -> None:
    mappings, seeds = parse(file)

    ranges_part1 = [Range(s, s) for s in seeds]
    location_ranges = mappings.convert_seed_to_location(ranges_part1)
    print(min(r.start for r in location_ranges))

    ranges_part2 = [
        Range(seeds[i], seeds[i] + seeds[i + 1] - 1)
        for i in range(0, len(seeds) - 1, 2)
    ]
    location_ranges = mappings.convert_seed_to_location(ranges_part2)
    print(min(r.start for r in location_ranges))


def parse(file: Path) -> tuple[MappingSet, list[int]]:
    seeds: list[int] = []
    mapping_set = MappingSet()
    current_mapping = None

    for line in file.open():
        line = line.strip()
        if m := re.match(r"seeds:((?: \d+)+)", line):
            seeds = list(map(int, m.group(1).split()))
        elif m := re.fullmatch(r"([a-z]+)-to-([a-z]+) map:", line):
            if current_mapping is not None:
                mapping_set.mappings[current_mapping.source] = current_mapping
            current_mapping = Mapping(
                source=m.group(1),
                target=m.group(2),
            )
        elif len(line) > 0:
            assert current_mapping is not None, line
            dest, source, length = map(int, line.split())
            current_mapping.transformations.append(
                Transformation(
                    start=source,
                    end=source + length - 1,
                    shift=dest - source,
                )
            )
        elif len(line) == 0:
            ...
        else:
            assert False, line

    if current_mapping is not None:
        mapping_set.mappings[current_mapping.source] = current_mapping

    assert seeds
    return mapping_set, seeds
