# [Day 17: Pyroclastic Flow](https://adventofcode.com/2022/day/17)

Tetris like!

### Part 1
Classic implementation with single coordinates moving for the whole block, inner blocks are computed only for collision
detection and transferred to the chamber when the rock is blocked.

I use `cycle` to iterate infinitely on rocks and jets, combined with `enumerate` to keep trace of the indices.

### Part 2
1 billion rocks!

Need to find something periodic... Got it with rock kind, jet index and top chamber rows. I detect the first identical
state, and compute the height rise and the number of blocks between these two states.
I can compute the number n of periodic stacking needed to approach the desired huge amount, and the few rocks still 
needed to get the full number. This complementary amount is thrown in the chamber to know the complementary height.

Then just need to sum up the bottom layer, n times the height of a periodic layer, and the top layer.

Very quick computation for a big number result.