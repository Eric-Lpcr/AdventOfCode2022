# [Day 25: Full of Hot Air](https://adventofcode.com/2022/day/25)

Base 5 numeration, with digit offset.

I created a first class dedicated to the SNAFU problem.

Just stored the digits values as a list of integers and classic numeration with power of base will work.
Normalisation is needed only when converting to symbolic representation: we have to put back the integer digits
int the authorised interval ([-2, 2] here), adding or removing exceeding value to the next digit.

I overriden the `__add__` method (adding digits by their position) and got de facto the `sum` working on the problem 
input list.

I also overriden the `__str__` and `__int__` to provide symbolic representation and conversion to base 10 number.

Finally, in order to test my class with provided examples, I implemented the `__eq__` to compare a SNAFU to another one,
or to a string or an integer.

### Reusable
Later I generalised the solution to any `BaseDecimal` in [base_decimal.py](../utilities/base_decimal.py) with its base, 
offset, symbols, prefix, suffix and operations expected from a number (arithmetic, logic).

I used `functools.@total_ordering` to gain all logic operators from `__eq__` and `__lt__`.

