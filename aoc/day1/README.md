# AOC 2023, day 1

My solution is just use a regular expression to catch the first number (digit or letters):

```
/(one|two|...|1|2|...)/
```

To catch the last number, we use the regular expression in reverse, by reversing the pattern and the string.

Another implementation to catch the last number:

```python
mapping = {
    "one": 1,
    "two": 2,
    # ...
    "1": 1,
    "2": 2,
    # ...
}

def extract_last(s: str) -> str:
    pos = -1
    val = None
    for k, v in mapping.items():
        p = s.rfind(k)
        if p > pos:
            pos = p
            val = v
    assert val is not None, s
    return str(val)
```
