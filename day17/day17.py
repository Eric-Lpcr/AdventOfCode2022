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
        self.jet_iterator = cycle(enumerate(-1 if jet == '<' else 1 for jet in self.jets))  # gives (jet_index, jet)
        self.jet_index = 0
        self.rock_count = 0
        self.rock_patterns = rock_patterns
        self.rock_iterator = iter(
            enumerate(  # gives (rock_count, ...)
                cycle(enumerate(  # gives (rock_index, rock)
                    Rock(pattern) for pattern in self.rock_patterns)), start=1))
        self.blocks = set()

    def throw_rocks(self, rock_amount, from_position):
        seen_states = dict()
        state_lines_count = 3

        for _ in range(rock_amount):
            self.rock_count, (rock_index, rock) = next(self.rock_iterator)
            self.throw_rock(rock, from_position)

            next_state = (rock_index+1, self.jet_index+1, self.to_string(state_lines_count))
            if next_state in seen_states:
                seen_states[next_state].append((self.rock_count, self.height))
                print(f'> Pattern found after {self.rock_count} rocks')
                break
            else:
                seen_states[next_state] = [(self.rock_count, self.height)]
        else:  # no pattern found, all rocks processed
            return self.height

        (rock_count1, height1), (rock_count2, height2) = seen_states[next_state]
        rock_period = rock_count2 - rock_count1
        height_period = height2 - height1

        total_height = height1  # before first pattern

        pattern_repetitions = (rock_amount - rock_count1) // rock_period
        total_height += height_period * pattern_repetitions

        remaining_rock_amount = (rock_amount - rock_count1) % rock_period
        for _ in range(remaining_rock_amount):
            self.rock_count, (rock_index, rock) = next(self.rock_iterator)
            self.throw_rock(rock, from_position)
        total_height += self.height - height2

        return total_height

    def throw_rock(self, rock, from_position):
        rock.place(from_position[0], from_position[1] + self.height)
        while rock.bottom >= 0:
            self.jet_index, jet = next(self.jet_iterator)
            rock.move(jet, 0)
            if rock.left < 0 or rock.right >= self.width or any(block in self.blocks for block in rock.blocks):
                rock.move(-jet, 0)
            rock.move(0, -1)
            if rock.bottom < 0 or any(block in self.blocks for block in rock.blocks):
                rock.move(0, 1)
                break
        self.blocks.update(rock.blocks)
        self.height = max(self.height, rock.top + 1)

    def to_string(self, top_lines=-1):
        result = ''
        for y in reversed(range(self.height)):
            result += ''.join('#' if (x, y) in self.blocks else '.' for x in range(self.width)) + '\n'
            top_lines -= 1
            if top_lines == 0:
                break
        return result

    def print(self, top_lines=-1):
        print(self.to_string(top_lines))


def main(filename, testing=False, expected1=None, expected2=None):
    print(f'--------- {filename}')

    with open(filename) as f:
        jets = f.readline().strip()

    chamber = Chamber(Rock_patterns, jets, width=7)
    result1 = chamber.throw_rocks(rock_amount=2022, from_position=(2, 3))
    print(f"Part 1: maximum height is {result1}")
    if testing and expected1 is not None:
        assert result1 == expected1

    chamber = Chamber(Rock_patterns, jets, width=7)
    result2 = chamber.throw_rocks(rock_amount=1_000_000_000_000, from_position=(2, 3))
    print(f"Part 2: maximum height is {result2}")
    if testing and expected2 is not None:
        assert result2 == expected2


if __name__ == '__main__':
    main('test.txt', True, 3068, 1_514_285_714_288)
    main('input.txt')
