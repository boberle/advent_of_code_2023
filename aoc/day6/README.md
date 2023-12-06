# AOC 2023, day 6

I just wanted to get to the second part to see what it was like, so I just wrote a short script to try all the possibilities without thinking about it. It appears that the script also work for the second part, while waiting less than 8 seconds on an old computer, so... Yeah, it's not the "official" way to solve it, but whatever.

One way to improve is to consider that there are 3 ranges of values (= the time during which you hold the button) between 0 and the race time _t_: one between 0 and _a_ for which you don't win, one between _a_ and _b_ for which you win, and one between _b_ and _t_ for which you don't win. Instead of computing the race result for each value between 0 and _t_, just compute _a_ and _b_. The computation time is divided by 3.5 times on my computer.

I should look for something better (binary search, or math), but I won't. I'll watch some videos on Internet instead.