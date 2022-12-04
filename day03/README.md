# [Day 3: Rucksack Reorganization](https://adventofcode.com/2022/day/3)

About sets and intersections.

### Set intersection

The `set.intersection` methode takes multiple sets as parameters. 
Intersection of a list of sets can be coded with:

    sets[0].intersection(*sets[1:])

or using an iterator object:

    next(sets_iter).intersection(*sets_iter)

### iterating n by n items

Got `grouper` itertool recipe From https://docs.python.org/fr/3.8/library/itertools.html#itertools-recipes

    def grouper(iterable, n, fill_value=None):
        """Collect data into fixed-length chunks or blocks"""
        # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
        args = [iter(iterable)] * n 
        return zip_longest(*args, fillvalue=fill_value)

 The trick resides in creating the `args` list containing the **same** iterator n times.
 zip will take an item in each arg (`n` for an iteration), so `n` consecutive items from the initial `iterable`.