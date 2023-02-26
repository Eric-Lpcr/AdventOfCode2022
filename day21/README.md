# [Day 21: Monkey Math](https://adventofcode.com/2022/day/21)

Binary tree.

### Part 1
Simple `Monkey` class which keeps the expression to compute. Each monkey is stored in a class variable tribe dictionary,
allowing the computation to find the monkey operands.

Just need to make 'root' monkey yell to get the result.

By the way, I didn't like the constructor with two forms, nor the double pattern test on input lines.

### Refactoring
I separated the monkeys in three kinds:
- the generic one which knows its name and its tribe
- the basic one which knows a value
- the smart one which knows an operation

Constructors parameters are better expressed than with a single class. I could also have set up factory methods,
but I'm fond of POO ;-)

I reviewed the documentation page for RE, and got a more explicit pattern with an alternative,
named groups (`(?P<name>...)`), verbose option and formatted string for the operators mastered by a SmartMonkey.

### Part 2
`Human` is a `BasicMonkey` which must compute its value, as expected by the tribe for the root monkey to be satisfied.

It is initialised with a NaN value which will lead all his dependent monkeys to yell NaN.

Solving is about finding the expected value for each monkey yelling Nan, starting from root, till human.




