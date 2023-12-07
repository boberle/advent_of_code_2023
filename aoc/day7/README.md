# AOC 2023, day 7

Nothing difficult with this one. To compute the type of the hand (five of kind, etc.), I use a `Counter` and check if there is a 5 in the counter values (for a five of a kind), a 4 (for a four of a kind), etc.

For the second part, the trick is to get the most frequent card (except `J`), and convert all the `J` to this card (if any).