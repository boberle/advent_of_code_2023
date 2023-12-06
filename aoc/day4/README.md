# AOC 2023, day 4

It's pretty simple. You can visualize the process with a table:

```
| card id | matching numbers | start  c1  c2  c3  c4  c5 | total |
|---------|------------------|---------------------------|-------|
| 1       | 4                | 1                         | 1     |
| 2       | 2                | 1      +1                 | 2     |
| 3       | 2                | 1      +1  +2             | 4     |
| 4       | 1                | 1      +1  +2  +4         | 8     |
| 5       | 0                | 1      +1      +4  +8     | 14    |
| 6       | 0                | 1                         | 1     |
```

At the start, you have one copy of each card.

At stage `c1`, you add the number of copies of card 1 (so 1) to the next 4 cards (because there are 4 matching numbers).

At stage `c2`, you add the number of copies of card 2 (so 2 in total) to the next 2 cards (because there are 2 matching numbers).

And so on.

Then you just sum up the `total` column.