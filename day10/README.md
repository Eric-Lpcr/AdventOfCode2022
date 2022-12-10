# [Day 10: Cathode-Ray Tube](https://adventofcode.com/2022/day/10)

About accumulation and indexing.

Decoded data is an accumulation of both cycle_consumption and register increment (addx parameter, 0 for noop), 
giving a list of tuples (start_of_cycle, register_value).

As I generalised the sampling function in part 1, it was fully reusable in part 2. But there was a bug when 
selecting a null value, which was erroneously considered not found.

I refactored the sampling function as a generator and changed the test with `ìn` containment operator instead of
relying on `dict.get` None result. See differences between [day_09_1.py](day_09_1.py) and [day_09.py](day_09.py).
