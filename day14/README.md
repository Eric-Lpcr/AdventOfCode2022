# [Day 14: Regolith Reservoir](https://adventofcode.com/2022/day/14)

Classic cellular automata?

Used:
- `namedtuple` to get x and y field names on coordinates
- separate sets for rock and sand, don't really know why, but at least it helped to clear the sand for part 2
- a cache of top y positions for each x, helping to make sand fall directly to the first obstacle

For part 2, I clarified the code by extracting some `Cave` methods, and creating a test `at` method enriched
with the infinite bottom test.

### Optimisation
Later I read a solution using complex numbers for position coding. I transposed my solution to [day14_complex.py]()
in order to evaluate whether it was faster... Didn't see a sensible difference... 
Also removed my 'fall to top' optimisation.

As I plotted the resting sand grain number over a grid paper, I noticed that each sand grain follows the same path as its
predecessor, except for the last move. I inserted a backtracking and wow, it gained a huge amount of processing time!

Oh, so lately discovered the `for: else:` construct, no need for "no move" boolean!