# [Day 16: Proboscidea Volcanium](https://adventofcode.com/2022/day/16)

Graphs again... This one made me rage quit at mid-December... and come back in January.

I got motivated to read and learn about graph algorithms, starting back with a clear knowledge of DFS, BFS, 
shortest path with Dijsktra and A*, recursion versus stacks and queues, all paths with Floyd-Warshall, and at last
the travelling salesman problem solved with backtracking.

I still need to work on flow algorithms, colouring, cuts, spanning trees... pfff.

# Part 1
The thing was about how to model the problem with a graph, having these minutes spent to travel between valves, 
to open them, or not... At first my graph was quite complicated, And I didn't figure how to walk inside towards
a solution.

Back to the problem! In fact we need to find the best opening *order* for the valves, going from one to another.
The cave map can be simplified to a complete graph linking all valves (interesting ones, starting AA, or with rate>0) 
by their distance. I used Floyd-Warshall algorithm to compute that (one could also use BFS for each starting valve).

Then we can explore all the permutations of valves, starting at AA. This is the travelling salesman problem: we need 
to explore all the valves successively, in any order. At each valve we know the elapsed time, it is open and liberates
a pressure amount which flows until the end of the allocated 30 minutes. This amount can be summed up on each path.
Once 30 minutes are elapsed, we can stop travelling and compare to the previous amount to keep the maximum.
It is to be noted that we need to check all the possibilities, there is no global stop criteria for the best solution
(like in shortest path computation between start and goal for example).

Hu, this one was hard!

# Part 2
Elephant helps.

I first started from part 1 and naively thought it would be simple to have two visitors in my salesman algorithm.
No way, they can never be studied at the same time (travel from different distances to valves) and my code became an
impossible mess.

I have to confess that I had a look to forums.

THe way to solve that is so simple!
We just need to think it as a combination of two disjoint partial paths having the optimal sum of pressure release.
We can reuse the part 1 algorithm and memorise the partial paths leading to each valve in all explored solutions, with 
their pressure got after 26 minutes if they were interrupted.

Then the solution is the couple of disjoint paths (no need for me and the elephant to open the same valve) having the
greater pressure sum.

But there is still an implementation complexity problem:
- with the example input, 7 valves give 1943 partial paths, and 1_886_653 combinations of 2 of them
- with the problem input, 54 valves give 430_875 partial paths, and **92_826_417_375** combinations of 2 of them!

My first implementation of path disjunction was using `set(path1).is_disjoint(set(path2))`. So slow...
At least I prepared the sets for all paths instead of computing them during `itertools.combinations` iteration, but it
was still slow. Again I read some solutions and found the classic bitmask trick which I had forgotten.
Just need to encode the opened valve on their dedicated bit, getting a mask for each path. The disjunction becomes a
so fast bitwise and `&`operation. 

Testing all the combinations still takes a long time on my old PC. I need to prune the combinations which in evidence 
can't contribute to a maximised pressure release (small paths travelling low rate valves).
As the combinations iterator keeps order, I sorted the paths in descending order of their pressure release, making the
solution appear faster. As we progressively found increasing maximums, we can stop the iteration as soon as the first
path of the pair contributes less than half of the current maximum (because the second path of the pair will be lower).
- with the example input, the search stops after 1_667_862 iterations: 218_791 were saved, 11%
- with the problem input, the search stops after 281_578_065 iterations: 92_544_839_310 were saved, **99.7%** !!!

### Performance improvements: 
1. Putting the memorisation of the paths before testing for time limit was counter performant, generating a
lot of useless invalid paths, with a huge impact when exploring the combinations for part 2.
2. Time limit to exit the part 1 exploration can be decreased by 2 minutes, as it is useless to travel 1 minute, open a
valve in another minute and generate no pressure exit as the time is elapsed.
3. Instead of computing all the shortest paths between all valves on the cave map, we could optimise the map by pruning
the unuseful valves and replacing their edges with longer ones between their neighbors.
For example, `AA(0)--(1)--II(0)--(1)--JJ(21)` can be simplified to `AA(0)--(2)--JJ(21)`, removing `II`.

On the problem input, before correction: 430875 paths gave 98e9 combinations, 280e6 were explored in 200 seconds.

After correction: 19689 paths give 193e6 combinations, shortened to 1.3e6 explored in 2 seconds!

The third improvement doesn't give significant performance gain as it impacts only the Floyd-Warshall computation.
Other explorations were already made on valve having a not null pressure rate. 

4. Using `itertools.combinations` in part 2 doesn't allow to break enough. I replaced it with two nested loop and coded 
a break condition for each one.

After correction: 19689 paths give 193e6 combinations, shortened to **7679** explored in 1,5 seconds. Not so much gain
(at least not aligned with the ratio of the iteration counts), I guess it's because I replaced a loop over a C 
implementation of combinations by a pure Python loop with a test.

# Reusable

Learnings on graphs, some links:
http://formations.telecom-bretagne.eu/pyrat/ in French, lot of articles
https://iq.opengenus.org/list-of-graph-algorithms/ in English

#### BFS
On unweighted graphs, gives the shortest paths from start node to all others (start to *), 
can stop when finding the goal. Flooding algorithm, gives consecutively all nodes at the same distance of start. 
#### Diskstra
On weighted graph, gives the shortest paths (start to *), can stop when goal is reached.
#### A*
Same than Diskstra, but options are prioritised according to a heuristic (for example, when moving on a grid, 
exploring first the nodes in the direction of the goal).
#### Floyd-Warshall
Gives all the paths and distances from any node to another (* to *).

#### A `graph` module
Capitalised in `utilities`, largely inspired from https://www.redblobgames.com/pathfinding/a-star/