# [Day 19: Not Enough Minerals](https://adventofcode.com/2022/day/19)

Planning problem.
I always wonder what was the best strategy for RTS 
[Real Time Strategy](https://en.wikipedia.org/wiki/Real-time_strategy) games.

I search and read about this subject:
- Googled "Planning for resource production in real-time strategy games"
- [Maximization of the Resource Production in RTS
Games using Planning and Scheduling](http://worldcomp-proceedings.com/proc/p2015/ICA2938.pdf)
- [Food, Gold, and Beyond: Exploring Multiple Means of Generating Resources in RTS 
Games](https://waywardstrategy.com/2022/01/23/food-gold-and-beyond/)
- [How do we improve resource harvesting in RTS 
games?](https://waywardstrategy.com/2019/12/04/resource-harvesting-in-rts/)
- Googled "Scheduling problem algorithm"
- [MIT 6.046J Design and Analysis of Algorithms, Spring 
2015](https://www.youtube.com/playlist?list=PLUl4u3cNGP6317WaSNfmCvGym2ucw3oGp)
- Googled "Dynamic programming"
- [What is Dynamic Programming? Working, Algorithms, and 
Examples](https://www.spiceworks.com/tech/devops/articles/what-is-dynamic-programming/)
- Googled "Cours ordonnancement PDF" (in french)

Pfff, really so complicated to me. I'd have really liked to program this problem as I would
do it by hand, adding robots for resources which are most needed and trying to compact every activity like I do it at
work  with Gantt or Pert diagrams.

I finally ended in starting it with an exploration instead of an optimisation.

### Part 1
Let's go for a DFS, as we must quickly find a complete solution to be able to early cut off branches.

State for each step is made with time left, robots and resources of each type.

At each step, I look at the delay for the factory to build a new robot, giving priority to high-value robots and
directly time forward to the next build (no need to check every minute). 

I coded arithmetics for resources (number of each material, number of robots, factory cost) in order to get clear code.
Defining an `__iter__` method yielding each property allows to vectorise the operations.

Ok, everything's ready for exploration. Wow, combinatorial complexity seems huge, this needs some cut-offs.
1. The obvious time limit: it's useless to build a robot during the last minute 
2. No need to build another robot of a kind when all its colleagues already produce the most expensive cost 
3. Kill the branch if even in the most favorable case (building a geode robot each remaining minute) wouldn't mine more
geodes than the previous best solution found. Here is the interest of DFS and high-value robot priority to early 
maximise the best solution till now.

### Part 2
Longer play time, but three first blueprints only. 
My solution takes a bit more time, but it's still acceptable. I guess that all my object arithmetic is 
counter-performant, but I find it elegant.

### Reusable
- Another experience on exploration.
- `__iter__` and yield
