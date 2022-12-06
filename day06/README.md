# [Day 6: Tuning Trouble](https://adventofcode.com/2022/day/6)

About sliding window (n-wise iteration) and all-unique list.

Got back some code from last year advent, day 1.

### Optimising execution time
I wondered if there was any optimisation about detecting uniqueness of all elements in a marker, and
tried a fast exit algorithm with `any` and a growing set of already seen elements.

Execution time measurements shows that the classic len(set(marker)) == len(marker) remains faster 
on the current problem input. I guess that pythonic implementation takes longer than builtin functions.

Looking for optimal implementation, the point is mainly about keeping track of previously read characters
instead of extracting 4 or 14 characters each time.

### Tribute to David
I like the principle of this ingenious solution from David Spiller:
https://github.com/dspi/ZTM_AdventOfCode2022/blob/main/day06/tuning_trouble.py

If the next character is already in the last seen characters, then the accumulated marker can be reduced after
its position. 
