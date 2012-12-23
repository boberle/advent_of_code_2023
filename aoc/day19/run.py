import operator
import re
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Callable

LIST = list(range(1, 4001))


@dataclass
class Part:
    x: int
    m: int
    a: int
    s: int

    @property
    def total(self) -> int:
        return self.x + self.m + self.a + self.s


class Operator(str, Enum):
    lt = "<"
    gt = ">"


@dataclass
class Rule:
    category: str
    operator: Operator
    value: int
    target: str


@dataclass
class Workflow:
    name: str
    rules: list[Rule]
    default: str

    def check(self, part: Part) -> str:
        cat2f = dict(
            x=operator.attrgetter("x"),
            m=operator.attrgetter("m"),
            a=operator.attrgetter("a"),
            s=operator.attrgetter("s"),
        )
        lt: Callable[[int, int], bool] = lambda a, b: a < b
        gt: Callable[[int, int], bool] = lambda a, b: a > b
        op2f = {
            Operator.lt: lt,
            Operator.gt: gt,
        }
        for rule in self.rules:
            if op2f[rule.operator](cat2f[rule.category](part), rule.value):
                return rule.target
        return self.default


def run(file: Path) -> None:
    parts, workflows = parse(file)
    name2workflow: dict[str, Workflow] = {w.name: w for w in workflows}

    accepted = get_accepted_parts(parts, name2workflow)
    total = 0
    for part in accepted:
        total += part.total
    print(total)

    root = Node(
        x=set(LIST),
        m=set(LIST),
        a=set(LIST),
        s=set(LIST),
    )
    terminals = get_accepted_terminals(name2workflow, "in", root)

    total = 0
    for terminal in terminals:
        comb = len(terminal.x) * len(terminal.m) * len(terminal.a) * len(terminal.s)
        total += comb
    print(total)


def parse(file: Path) -> tuple[list[Part], list[Workflow]]:
    parts = []
    workflows = []
    for line in file.open():
        line = line.strip()
        if m := re.fullmatch(r"(\w+)\{(.+)\}", line):
            split = m.group(2).split(",")
            rules: list[Rule] = []
            for i, r in enumerate(split):
                if i == len(split) - 1:
                    workflows.append(
                        Workflow(
                            name=m.group(1),
                            rules=rules,
                            default=r,
                        )
                    )
                else:
                    m2 = re.fullmatch(r"([xmas])([<>])(\d+):(\w+)", r)
                    assert m2
                    rules.append(
                        Rule(
                            category=m2.group(1),
                            operator={"<": Operator.lt, ">": Operator.gt}[m2.group(2)],
                            value=int(m2.group(3)),
                            target=m2.group(4),
                        )
                    )
        elif m := re.fullmatch(r"\{(.+)\}", line):
            categories = dict()
            for m in re.finditer(r"([xmas])=(\d+)", m.group(1)):
                categories[m.group(1)] = int(m.group(2))
            parts.append(Part(**categories))

    return parts, workflows


def get_accepted_parts(parts: list[Part], workflows: dict[str, Workflow]) -> list[Part]:
    accepted: list[Part] = []
    for part in parts:
        if process_part(workflows, part):
            accepted.append(part)
    return accepted


def process_part(workflows: dict[str, Workflow], part: Part) -> bool:
    w = workflows["in"]
    while True:
        res = w.check(part)
        if res == "A":
            return True
        elif res == "R":
            return False
        else:
            w = workflows[res]


@dataclass
class Node:
    x: set[int] = field(default_factory=set)
    m: set[int] = field(default_factory=set)
    a: set[int] = field(default_factory=set)
    s: set[int] = field(default_factory=set)

    def new(
        self,
        x: set[int] | None = None,
        m: set[int] | None = None,
        a: set[int] | None = None,
        s: set[int] | None = None,
    ) -> "Node":
        return Node(
            x=set(x) if x is not None else self.x,
            m=set(m) if m is not None else self.m,
            a=set(a) if a is not None else self.a,
            s=set(s) if s is not None else self.s,
        )


def get_accepted_terminals(
    workflows: dict[str, Workflow], workflow_name: str, node: Node
) -> list[Node]:
    rv = []
    for rule in workflows[workflow_name].rules:
        values = getattr(node, rule.category)
        if rule.operator == Operator.lt:
            new_values = values & set(LIST[: rule.value - 1])
            old_values = values & set(LIST[rule.value - 1 :])
        else:
            old_values = values & set(LIST[: rule.value])
            new_values = values & set(LIST[rule.value :])
        new_node = node.new(**{rule.category: new_values})
        setattr(node, rule.category, old_values)
        if rule.target == "A":
            rv.append(new_node)
        elif rule.target == "R":
            pass
        else:
            rv.extend(get_accepted_terminals(workflows, rule.target, new_node))

    if workflows[workflow_name].default == "A":
        rv.append(node)
    elif workflows[workflow_name].default == "R":
        pass
    else:
        rv.extend(
            get_accepted_terminals(workflows, workflows[workflow_name].default, node)
        )

    return rv
