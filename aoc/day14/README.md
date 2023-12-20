# AOC 2023, day 14

For the second part, we note that iterations for a same load produces arithmetic sequences. For the example given in the statement, we have (for the first few iterations):

```python
{
    63: [8, 15, 22, 29, 36, 43, 50, 57, 64],
    64: [6, 13, 20, 27, 34, 41, 48, 55, 62],
    65: [5, 7, 12, 14, 19, 21, 26, 28, 33, 35, 40, 42, 47, 49, 54, 56, 61, 63],
    68: [9, 16, 23, 30, 37, 44, 51, 58, 65],
    69: [2, 3, 4, 10, 11, 17, 18, 24, 25, 31, 32, 38, 39, 45, 46, 52, 53, 59, 60, 66, 67],
    87: [1],
}
```

where the keys (63, 64, 65, etc.) are the loads and the numbers in the list are the iterations that produces that load. For example, at iterations 8, 15, 22, etc., we have a load of 63.

Note that most of the lists are arithmetic sequences. This means that it is easy to find the load at 1000000000, we just need to find in which sequence this number is. To do that, we run the cycles until we get an arithmetic sequence that fulfill this formula:

```
(1000000000 - init) % diff == 0
```

where `init` is the initial term of the sequence and `diff` the difference between each term of the sequence.

In the example, we note that

```
(1000000000 - 6) % 7 == 0
```

So `64` is the load at 1000000000 iterations.