# AOC 2023, day 11

We read the coordinates of each galaxy. Then for each empty row/column, we add `n` to the following `x` and `y` of each galaxy, where `n` is `1` for the first part, and `1000000-1` for the second part.

Then we just compute the Manhattan distance between each pair of galaxies, and we divide by 2 because the order it not important (`a -> b` is equal to `b -> a`).