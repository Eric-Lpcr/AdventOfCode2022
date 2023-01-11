# [Day 15: Beacon Exclusion Zone](https://adventofcode.com/2022/day/15)

Diamonds are forever...

## Part 1
A bit of geometry to compute the intersection of a diamond and an horizontal line, 
storing the result in inclusive intervals (ranges), according to the vertical distance 
from the line to the diamond center. 

Next problem is to combine ranges which overlap
in order to count only once common positions. This is done by iterating ranges sorted by their lower
bound and extending them to the next one upper bound if the next lower bound is inside the current
range. For example, `[2, 7]` followed by `[5, 8]`: `5` is inside `[2, 7]`, so we keep `[2, 8]` and so on.

## Part 2
The searched position needs to be outside all sensor diamonds (i.e. manhattan distance > 
sensor range), but as it is unique, it must be situated just next to a diamond border. 
Instead of scanning all the space, we can iterate on diamonds borders (sensor range + 1) 
and stop as soon as we find a position not contained in any sensor range.

## Reusable
An `InclusiveRange` class, which could be improved to behave like the `range` object 
(generator, step...), and generalised to manage inclusive / exclusive edges.

I also definitely capitalise a 2D coordinate class. Here I used a simple `namedtuple`