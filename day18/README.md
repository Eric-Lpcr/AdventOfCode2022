# [Day 18: Boiling Boulders](https://adventofcode.com/2022/day/18)

3D graphics

### Part 1
I did it first without neighborhood exploration, just combining the lava droplet cubes by pairs. If they are not distant
(manhattan distance) more than one, then they share a face and each of them number of free faces can be decremented.

### Part 2
I computed a bounding box, added a margin of 1, and flood filled it with a BFS traversal. Each time a neighbor is a
part of the lava droplet, then its surface is augmented by one.

That's also the way you can measure an object volume: put it in a defined volume of water, and measure the volume
increase.

I finally reworked the part 1 to simply check the neighbors of each lava droplet cube. Much simpler!

### Reusable
I generalised a `Coordinate` class in `utilities`, having common code for 2D and 3D decimal or float coordinates.

Also added the itertools recipes from Python documentation in my utilities.
