# [Day 13: Distress Signal](https://adventofcode.com/2022/day/13)

About comparison of different types, ordering.

Decoding was trivial using `eval` as the packet input syntax is pythonic.

I implemented two packet classes, one for single integer content, another one for list, and converted the list of
list input using a factory build method.

I augmented the two classes with `<` and `==` operators, `@functools.totalordering` annotation generates all the other
comparison operators. The solution was two allow comparison of an integer packet with a list packet, based on the fact
that lists already compare one to another one.

For part 2, I converted the list of packet pairs to a list of all packets using `itertools.chain`, adding dividers.
The list is fully sortable with `sort` or `sorted` because elements are comparable with the operator `<`, 
and containment with`ìn` is also available because of the operator `==` working on elements.

### Improvements
I did try to hack list and int comparison operators, but these classes are immutable types. 
I also tried to simplify the code by inheriting my classes from int and list, but then _totalordering_ was not working
and I would have had to overload all comparison operators (my classes were inheriting bad behavior...) and code
would have become longer.

I finally wrote a compact non object version with a `compare` function in [day13_compare.py](). `functools.cmp_to_key` allows to
convert such a function to a key for `sort` or `sorted`.

Better use `list.index` for part 2!