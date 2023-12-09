from dataclasses import dataclass
from pathlib import Path


@dataclass
class History:
    seq: list[int]


def run(file: Path) -> None:
    histories = parse(file)
    print(sum(predict(history.seq) for history in histories))
    print(sum(predict(history.seq, backwards=True) for history in histories))


def parse(file: Path) -> list[History]:
    return [History(seq=list(map(int, line.split()))) for line in file.open()]


def predict(seq: list[int], backwards: bool = False) -> int:
    assert len(seq) > 1
    diffs, is_zero = compute_diffs(seq)
    if is_zero:
        if backwards:
            return seq[0]
        else:
            return seq[-1]
    if backwards:
        return seq[0] - predict(diffs, backwards=backwards)
    else:
        return seq[-1] + predict(diffs, backwards=backwards)


def compute_diffs(seq: list[int]) -> tuple[list[int], bool]:
    diffs = []
    is_zero = True
    for i in range(1, len(seq)):
        d = seq[i] - seq[i - 1]
        diffs.append(d)
        if d != 0:
            is_zero = False
    return diffs, is_zero
