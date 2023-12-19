# AOC 2023, day 13

To find the mirror columns, we just check every column. For each column, we check if every point has a mirror point (if the expected mirror point is in the limit of the game board, otherwise we ignore it).  We must have 0 missed point for the first point, and exactly 1 for the second part (the smudge).  We do exactly the same to find the mirror rows.