from collections import defaultdict
from enum import IntEnum


class Figure(IntEnum):
    Rock = 1
    Paper = 2
    Scissors = 3


class Score(IntEnum):
    Loss = 0
    Draw = 3
    Win = 6


class Game:
    rules = {
        (Figure.Rock, Figure.Rock): (Score.Draw, Score.Draw),
        (Figure.Rock, Figure.Paper): (Score.Loss, Score.Win),
        (Figure.Rock, Figure.Scissors): (Score.Win, Score.Loss),
        (Figure.Paper, Figure.Rock): (Score.Win, Score.Loss),
        (Figure.Paper, Figure.Paper): (Score.Draw, Score.Draw),
        (Figure.Paper, Figure.Scissors): (Score.Loss, Score.Win),
        (Figure.Scissors, Figure.Rock): (Score.Loss, Score.Win),
        (Figure.Scissors, Figure.Paper): (Score.Win, Score.Loss),
        (Figure.Scissors, Figure.Scissors): (Score.Draw, Score.Draw),
    }

    def play(self, turns):
        scores = map(self.play_turn, turns)
        # final_score = reduce(lambda x, y: (x[0] + y[0], x[1] + y[1]), scores, (0, 0))
        # final_score = sum(map(itemgetter(0), scores)),
        #               sum(map(itemgetter(1), scores))  # WRONG: first map consumes scores...
        final_score = tuple(map(sum, zip(*scores)))  # zip converts list of tuples to tuple of lists
        return final_score

    def play_turn(self, turn):
        # returns a couple of scores from a couple of figures
        w1, w2 = self.rules.get(turn)  # battle score
        f1, f2 = turn  # figure score
        return w1 + f1, w2 + f2


def decode_input_part1(input_data):
    key = {'A': Figure.Rock, 'B': Figure.Paper, 'C': Figure.Scissors,
           'X': Figure.Rock, 'Y': Figure.Paper, 'Z': Figure.Scissors}
    return map(lambda encoded_turn: (key.get(encoded_turn[0]), key.get(encoded_turn[1])), input_data)


def decode_input_part2(input_data):
    key = {'A': Figure.Rock, 'B': Figure.Paper, 'C': Figure.Scissors,
           'X': Score.Loss, 'Y': Score.Draw, 'Z': Score.Win}
    decoded_turns = map(lambda encoded_turn: (key.get(encoded_turn[0]), key.get(encoded_turn[1])), input_data)

    expected_figure = defaultdict(dict)
    for (against_figure, figure_to_play), (_, expected_result) in Game.rules.items():
        expected_figure[expected_result][against_figure] = figure_to_play
    turns = map(lambda decoded_turn: (decoded_turn[0], expected_figure.get(decoded_turn[1]).get(decoded_turn[0])),
                decoded_turns)
    return turns


def solve_problem(filename, expected1=None, expected2=None):
    print(f'--------- {filename}')

    with open(filename) as f:
        input_data = [line.split() for line in f.readlines()]

    turns = decode_input_part1(input_data)
    scores = Game().play(turns)

    result1 = scores[1]
    print(f"Part 1: strategy guide score is {result1}")
    if expected1 is not None:
        assert result1 == expected1

    turns = decode_input_part2(input_data)
    scores = Game().play(turns)

    result2 = scores[1]
    print(f"Part 2: strategy guide score is {result2}")

    if expected2 is not None:
        assert result2 == expected2


def main():
    solve_problem('test.txt', 15, 12)
    solve_problem('input.txt', 12276, 9975)


if __name__ == '__main__':
    main()
