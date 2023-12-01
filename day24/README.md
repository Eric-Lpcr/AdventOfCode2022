# [Day 24: Blizzard Basin](https://adventofcode.com/2022/day/24)


### Part 1


```
b = 0          # The empty bitset :)
b |= 1 << i    # Set
b & 1 << i     # Test
b &= ~(1 << i) # Reset
b ^= 1 << i    # Flip i
b = ~b         # Flip all
```

### Part 2
