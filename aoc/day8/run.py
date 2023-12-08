from __future__ import annotations

import math
import re
from dataclasses import dataclass, field
from enum import Enum, auto
from itertools import cycle
from pathlib import Path


@dataclass
class Node:
    id: str
    left: Node | None = None
    right: Node | None = None


class Turn(int, Enum):
    R = auto()
    L = auto()


@dataclass
class SandPath:
    turns: list[Turn] = field(default_factory=list)


def run(file: Path) -> None:
    sand_path, start_nodes = parse(file)

    periods: list[int] = []
    for node in start_nodes:
        if node.id == "AAA":
            print("part 1", walk(sand_path, node))
        periods.append(find_period(sand_path, node))
    print("part 2", math.lcm(*periods))


def parse(file: Path) -> tuple[SandPath, list[Node]]:
    path = SandPath()

    nodes: dict[str, tuple[str, str]] = dict()
    for i, line in enumerate(file.open()):
        if i == 0:
            for c in line.strip():
                path.turns.append(Turn[c])
        elif i == 1:
            pass
        else:
            m = re.fullmatch(r"(\w+) = \((\w+), (\w+)\)", line.strip())
            assert m, line
            nodes[m.group(1)] = (m.group(2), m.group(3))

    id2node: dict[str, Node] = {id: Node(id=id) for id, _ in nodes.items()}

    for id, (left, right) in nodes.items():
        # possible memory leak
        id2node[id].left = id2node[left]
        id2node[id].right = id2node[right]

    return path, [node for name, node in id2node.items() if name.endswith("A")]


def walk(path: SandPath, start_node: Node) -> int:
    cur = start_node
    for i, turn in enumerate(cycle(path.turns)):
        if turn == Turn.L:
            assert cur.left is not None
            cur = cur.left
        else:
            assert cur.right is not None
            cur = cur.right
        if cur.id == "ZZZ":
            return i + 1
    assert False


def find_period(path: SandPath, start_node: Node) -> int:
    cur = start_node
    for i, turn in enumerate(cycle(path.turns)):
        if turn == Turn.L:
            assert cur.left is not None
            cur = cur.left
        else:
            assert cur.right is not None
            cur = cur.right
        if cur.id.endswith("Z"):
            return i + 1
    assert False
