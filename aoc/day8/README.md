# AOC 2023, day 8

For the first part, we just need to parse the network into a data structure that accept references, like:

```python
@dataclass
class Node:
    id: str
    left: Node
    right: Node
```

Then just start with the node `AAA` and follow the path using the `left` or `right` attribute according to the turn, and count the number of turns until you reach the node `ZZZ`.

For the second part, we do the same for each node that ends with an `A`, stopping at the first node that ends with a `Z`. We have a bunch of numbers that correspond to "periods", which means that the path repeats itself after `n` turns (`n` being the period).

And then, we just compute the LCM (Least Common Multiple) of all the periods. Thank God, Python as a builtin `lcm` function!
