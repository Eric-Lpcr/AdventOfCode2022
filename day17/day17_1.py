from operator import itemgetter

from itertools import cycle

Rock_patterns = [
    [(0, 0), (1, 0), (2, 0), (3, 0)],  # minus
    [(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)],  # plus
    [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)],  # angle
    [(0, 0), (0, 1), (0, 2), (0, 3)],  # vertical bar
    [(0, 0), (1, 0), (0, 1), (1, 1)],  # square
]


class Rock:
    def __init__(self, pattern):
        self.pattern = pattern
        self.left = self.bottom = 0
        self.width = max(map(itemgetter(0), self.pattern)) + 1
        self.height = max(map(itemgetter(1), self.pattern)) + 1

    @property
    def right(self):
        return self.left + self.width - 1

    @property
    def top(self):
        return self.bottom + self.height - 1

    def move(self, dx, dy):
        self.left += dx
        self.bottom += dy

    def place(self, x, y):
        self.left = x
        self.bottom = y

    @property
    def blocks(self):
        return ((x + self.left, y + self.bottom) for x, y in self.pattern)

    def __repr__(self):
        return str((self.left, self.bottom))


class Chamber:
    def __init__(self, rock_patterns, jets, width=7):
        self.width = width
        self.height = 0
        self.jets = jets
        self.jet_iterator = cycle(-1 if jet == '<' else 1 for jet in self.jets)
        self.rock_patterns = rock_patterns
        self.rock_iterator = cycle(Rock(pattern) for pattern in self.rock_patterns)
        self.blocks = set()

    def throw_rocks(self, times, from_position):
        for _ in range(times):
            rock = next(self.rock_iterator)
            self.throw_rock(rock, from_position)
            # self.print()

    def throw_rock(self, rock, from_position):
        rock.place(from_position[0], from_position[1] + self.height)
        while rock.bottom >= 0:
            jet = next(self.jet_iterator)
            rock.move(jet, 0)
            if rock.left < 0 or rock.right >= self.width or any(block in self.blocks for block in rock.blocks):
                rock.move(-jet, 0)
            rock.move(0, -1)
            if rock.bottom < 0 or any(block in self.blocks for block in rock.blocks):
                rock.move(0, 1)
                break
        self.blocks.update(rock.blocks)
        self.height = max(self.height, rock.top + 1)

    def print(self, top=-1):
        for y in reversed(range(self.height)):
            print(''.join('#' if (x, y) in self.blocks else '.' for x in range(self.width)))
            top -= 1
            if top == 0:
                break


def main(filename, testing=False, expected1=None, expected2=None):
    print(f'--------- {filename}')

    with open(filename) as f:
        jets = f.readline().strip()

    chamber = Chamber(Rock_patterns, jets, width=7)
    chamber.throw_rocks(times=2022, from_position=(2, 3))
    result1 = chamber.height
    print(f"Part 1: maximum height is {result1}")
    if testing and expected1 is not None:
        assert result1 == expected1

    result2 = 0
    print(f"Part 2: {result2}")
    if testing and expected2 is not None:
        assert result2 == expected2


if __name__ == '__main__':
    main('test.txt', True, 3068, None)
    main('input.txt')
