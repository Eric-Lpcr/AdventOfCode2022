# [Day 8: Treetop Tree House](https://adventofcode.com/2022/day/8)

About matrices, lines and columns, line of sight.

I used list of lines to store data. 
When column processing is needed, I transpose using `zip(*data)` before computing, and transpose back the result.

### Part 1
I implemented a simple processing for visibility of trees when seen from the West.
To see the forest from the East side, I flip the lines with a `reversed` iterator, and flip back the result.
To see it from North needs a transposition. South view needs a transposition and a flip.

I combined the 4 visibility matrices with an item wise boolean or and count the number of True values.

### Part 2
This second part seems to be another problem at all!
I compute the score line by line for each tree, horizontally first. 
Then I transpose the forest to apply the same scoring method to colums, and transpose back 
the result. 
I finally combine the two scoring matrices with an item wise `mul` operator and get the maximum value.