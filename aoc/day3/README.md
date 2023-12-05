# AOC 2023, day 3

We parse the numbers as by recording their value and their positions in the coordinate system: start x, end x and y (the top left corner is `0, 0`). For example, the `633` in the example will have the following properties:

```
value: 633
x1 (start): 6
x2 (end): 8
y: 2
```

Then it's easy to check whether a number is adjacent to a symbol or not.