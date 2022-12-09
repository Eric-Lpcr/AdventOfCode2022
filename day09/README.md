# [Day 9: Rope Bridge](https://adventofcode.com/2022/day/9)

About cartesian coordinates.

I reused an older problem `Coordinate` class.

As the space is not defined, no grid is needed. The places visited by the rope tail are kept in a set.

I kept my Part 1 solution in [day_09_1.py](day_09_1.py). 
A `Rope` has a head a tail, the tail follows the head moves.

For part 2, a `Knot` class appears, which gets the responsibility to be moved and follow another knot. 
The `Rope` becomes a list of `Knot` and solution is generalized for part 1 and part 2.
