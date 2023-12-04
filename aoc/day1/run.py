import re
from pathlib import Path


def run(file: Path) -> None:
    t1 = 0
    t2 = 0
    for line in file.open():
        t1 += extract_digits(line)
        t2 += int(extract_first(line) + extract_last(line))
    print(t1, t2)


def extract_digits(s: str) -> int:
    s = re.sub(r"[^0-9]", "", s)
    return int(s[0] + s[-1])


mapping = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "1": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
}


def extract_first(s: str) -> str:
    m = re.search("(" + "|".join(mapping.keys()) + ")", s)
    assert m is not None
    return str(mapping[m.group(0)])


def extract_last(s: str) -> str:
    m = re.search("(" + "|".join(k[::-1] for k in mapping.keys()) + ")", s[::-1])
    assert m is not None
    return str(mapping[m.group(0)[::-1]])


def extract_last_other_implementation(s: str) -> str:
    pos = -1
    val = None
    for k, v in mapping.items():
        p = s.rfind(k)
        if p > pos:
            pos = p
            val = v
    assert val is not None, s
    return str(val)
