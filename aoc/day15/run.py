from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Box:
    lenses: dict[str, int] = field(default_factory=dict)

    def remove(self, label: str) -> None:
        if label in self.lenses:
            del self.lenses[label]

    def add(self, label: str, focal: int) -> None:
        self.lenses[label] = focal

    def compute_focusing_power(self, box_index: int) -> int:
        box_index += 1
        total = 0
        for i, focal in enumerate(self.lenses.values(), start=1):
            total += box_index * i * focal
        return total


def run(file: Path) -> None:
    steps = parse(file)
    print(sum((compute_hash(step) for step in steps)))

    boxes: list[Box] = [Box() for _ in range(256)]

    for step in steps:
        if "-" in step:
            label, _ = step.split("-")
            index = compute_hash(label)
            boxes[index].remove(label)
        elif "=" in step:
            label, focal_string = step.split("=")
            focal = int(focal_string)
            index = compute_hash(label)
            boxes[index].add(label, focal)
        else:
            assert False

    focusing_power = 0
    for i, box in enumerate(boxes):
        focusing_power += box.compute_focusing_power(i)
    print(focusing_power)


def compute_hash(s: str) -> int:
    total = 0
    for c in s:
        total += ord(c)
        total = (total * 17) % 256
    return total


def parse(file: Path) -> list[str]:
    content = file.read_text().strip()
    content = content.replace("\n", "")
    return content.split(",")
