# [Day 20: Grove Positioning System](https://adventofcode.com/2022/day/20)

Numbers mixing.

### Part 1
We need to move objects in a list, but still keeping the original order to iterate on them.

I chose to keep the list unmixed and to compute the position of elements after one moves. I wrapped the values in 
`NumberPosition` objects.
Each time an object moves, the objects at positions before or after its new one have to shift 1 or -1 depending
on the move.

Got it working with many code adjustments... But not so happy about code clarity.

### Part 2
Ok, having bigger numbers should not change anything as I managed moves with a modulo
of list length (initially for circular aspect of the moves).

Argghhhhh it failed for part 2 problem input and I couldn't imagine debugging...

Let's reexamine the problem:
- We need a data structure which keeps the order and indexation: list is ok
- We need another one which allows fast move (extract / insert) of elements: linked list will suit for that

Linked list in Python is `collections.deque`. 
It has no access by index, only pop or append on each edge. 

But wait I asked for help and found that `deque` offers a nice `rotate` method which
will nicely manage the circular behaviour.

The move can then be decomposed to:
1. put the desired element at front
2. remove it 
3. rotate at desired position 
4. reinsert it

As elements are moving in the linked list, we need to find their position to make the first step.
Looking up by number would be risky as we can't presume whether there is no multiple elements with the same value.
How to get them unambiguous: at first I kept my `NumberPosition` wrapper, which I replaced with a `namedtuple`. 
Identical numbers have different position, so they will be unique in the lists and `index` will work correctly. 

See my first working solution in [day_20_2.py](day_20_2.py)

### Improvements

Unicity is also possible by object identity instead of equality. I finally wrapped the number in an `Item` class which
has no equality operation (that was automatically generated for tuple, namedtuple or dataclass).

I thought that an efficient `deque.rotate` should manage rotations asking for many full turns and should reduce its
parameter to the length modulo.

Just checked in source code, and obviously it does:
[deque C source code](https://github.com/python/cpython/blob/main/Modules/_collectionsmodule.c#L777)

So I removed the modulo from my code, for a nice lighter implementation.
