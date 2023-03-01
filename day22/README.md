# [Day 22: Monkey Map](https://adventofcode.com/2022/day/22)

Moving on a grid... or not.

### Part 1
Classic implementation with a 2D grid and movement array constants.

I factorised the next position computation in a method which wraps around grid limits and also skips empty zones. 

The move instructions execution is just doing it step by step, halting when an obstacle is encountered.

[day22_1.py](day22_1.py)

### Part 2
Grid is a cube...

Ok, wrapping around empty zones is not the point anymore. I chose to prepare the neighbors from the edge of a face 
leading to another face, and depending on the orientation. It's a kind of hardcoded move which supersedes a regular one.

I refactored the part one to connect faces with the same mechanism, and it doesn't work anymore for the problem 
input... See [day22_2.py](day22_2.py)

Gosh, test data and input data doesn't have the same layout!
Ok, the problem is not so obvious, it's Day 22 after all!

Let's go, I have to analyse the input data:
- localise and identify the faces
- connect their edges

Face side size: a cube development layout always occupies a 4x3 or 3x4 grid.

Faces neighboring (volume, test data and input data example):
```
   A--------B               A---B               A---B---F
  /        /|               | 1 |               | 1 | 3 |
 / |      / |       B---A---D---C               D---C---G
D--------C  |       | 5 | 4 | 2 |               | 2 |
|  |     |  |       F---E---H---G---C       D---H---G
|  E - - | -F               | 6 | 3 |       | 4 | 6 |
| /      | /                E---F---B       A---E---F
|/       |/                                 | 5 |
H--------G                                  B---F
```
I chose to number the faces according to a die (sum of opposites is always 7) to have a numbering which doesn't depend
on the development layout, and I stored all the cube geometry facts in a reference class.

Assuming the first face found is ABCD, we can deduce the others, with the cube reference applied to neighbors explored
with a BFS.

One shall note that the faces edges are not labelled identically on the two examples (BAFE vs AEFB, or GCBF vs BFGC): 
this will support face orientation according to a particular cube development.

Once done, they share edges that we can connect with teleports, as planned initially.

I got my first working version in [day22_3.py](day22_3.py) and finally refactored my code to make it
more clear with enums and nice classes.
 
[day22.py](day22.py)

### Reusable
- Adding a property to enum values:  utilities.enums2.IntEnumWithProp
- Cube geometry