# AOC 2023, day 19

The trick to the second part is to recognize that the workflows and their rules are just a decision tree. So you just need to compute the possible ranges for each node, until you get to the bottom of the tree (the terminal nodes). Then you compute the number of combinations for each terminal node (which is just `|x|*|m|*|a|*|s|` where `|x|` is the cardinality of the set `x`) and sum up them all.

Here is an example based on the beginning of the example provided in the statement:

![](../../doc/day19.png)
