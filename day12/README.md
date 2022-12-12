# [Day 12: Hill Climbing Algorithm](https://adventofcode.com/2022/day/12)

Shortest path? Dijkstra? No, ___A*___ !

I remembered [2021 calendar, Day 15: Chiton](https://adventofcode.com/2021/day/15)
and my [comments](https://github.com/Eric-Lpcr/AdventOfCode2021/tree/master/day15):

> Oh no, graph again!
> And shortest path on a weighted graph... That immediately recalled me Dijkstra study 20 years ago during my late 
> university, with a professor asking us to unwind the algorithm manually and write down (yes, with a pen and a paper) 
> all the steps.
> I think I learned about the algorithm (it stayed in my mind), but I also get traumatized ;-(
> 
> And tonight I really don't enjoy implementing such a thing.
>
> So for one time, I'll do it like a serious lazy developer in the internet era: let's find a nice solution made by
> someone else. I'm a bit frustrated, but otherwise I won't succeed.
> 
> Better than Dijkstra when you know the exact destination is A* algorithm:
> [Introduction to the A* Algorithm](https://www.redblobgames.com/pathfinding/a-star/introduction.html).
>
> Ok, got an excellent code in [implementation.py](implementation.py) from 
> [Implementation of A*](https://www.redblobgames.com/pathfinding/a-star/implementation.html#python).

This time I wrote a `HeightGrid` class implementing the contract for the `a_star_search` function, and just called it.

Ok, part 1 solved, one more time not so proud of me but after all, reuse is also part of the job.

Part 2 is easy with this fast algorithm, just need to scan for starting points and apply the same method.
