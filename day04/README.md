# [Day 4: Camp Cleanup](https://adventofcode.com/2022/day/4)

About inclusive ranges, containment and overlapping.

Implemented with a simple `InclusiveRange` class, overriding `__contains__` to get the `in` operator syntax.

### Count-if in Python
Used the classic count-if trick `sum(map(<condition>, <iterable>))` summing a boolean generator, like in:

    sum(x % 2 for x in range(10))
    sum(map(is_even, range(10))  # assuming a is_even function exists

Because `len` can't work on generators and needs a conversion to a list

    len([x for x in range(10) if x % 2])

### Star abuse

    overlapping_pairs = (r1.overlap(r2) for (r1, r2) in input_data)

Could be coded:    

    overlapping_pairs = map(InclusiveRange.overlap, *zip(*input_data))

* `input_data` is a list of pairs of `InclusiveRange`
* `*input_data` gives all pairs to zip, first iteration will give all pairs first element,
second iteration will give all pairs second element
* `*zip` will give `map` two generators, one for first pair elements, another for second pair
elements
* `map` calling a two parameters function expects two lists

First syntax remains really more readable!