# [Day 2: Rock Paper Scissors](https://adventofcode.com/2022/day/2)

About decoding input and implementing game rules using tuples, enums and dictionnaries.

How to convert a list of tuples to a tuple of lists with `zip`:

    l = [('a', 1), ('b', 2), ('c', 3)]
    list(zip(*l))`
gives

    [('a', 'b', 'c'), (1, 2, 3)]

