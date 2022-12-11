# [Day 11: Monkey in the Middle](https://adventofcode.com/2022/day/11)

About operations, partials, modulus and for part 1 mostly decoding input to a usable storage.

Numbers are quickly getting huge in part 2, when no longer dividing by 3 after each inspection.

I first thought about storing the item worry level as a list of prime factors and handling operations smartly. 
But there's additions in the monkeys operations, which is not working with prime factor decompositions
(multiplying was adding factors, square was duplicating the list, but addition... no way).

in fact, the item worry level is significant for the problem only to be tested against each monkey divisor.
So it doesn't need to be greater than the product of all monkeys divisors (my `item_modulus` game attribute).
So it can be reduced at any moment to the remainder (modulus) of the division by this item_modulus.

Thanks to Reddit guys for the idea, I'm not fond of 
[Modular arithmetic](https://en.wikipedia.org/wiki/Modular_arithmetic), 
but it can drastically save time with monkeys. 
