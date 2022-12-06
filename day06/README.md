# [Day 6: Tuning Trouble](https://adventofcode.com/2022/day/6)

About sliding window (n-wise iteration) and all-unique list.

Got back some code from last year advent, day 1.

I wondered if there was any optimisation about detecting uniqueness of all elements in a marker, and
tried a fast exit algorithm with `any` and a growing set of already seen elements.

Execution time measurements shows that the classic len(set(marker)) == len(marker) remains faster 
on the current problem input. I guess that pythonic implementation takes longer than builtin functions.
