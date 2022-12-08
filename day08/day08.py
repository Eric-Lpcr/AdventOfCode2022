import operator
from itertools import islice


def visible_from_left(trees):
    """Returns a bool array telling whether the tree is visible from the left side"""
    highest_tree = ''
    visible = []
    for i, tree in enumerate(trees):
        if tree > highest_tree:
            visible.append(True)
            highest_tree = tree
        else:
            visible.append(False)
    return visible


def combine(list_of_lists_1, list_of_lists_2, binary_op):
    """Apply binary_op element-wise on list of lists"""
    visible = []
    for line1, line2 in zip(list_of_lists_1, list_of_lists_2):
        visible.append([binary_op(e1, e2) for e1, e2 in zip(line1, line2)])
    return visible


def visible_trees(forest):
    visible_from_w = [visible_from_left(trees) for trees in forest]  # West view is trivial

    visible_from_e = [list(reversed(visible_from_left(reversed(trees)))) for trees in forest]  # East needs reverse

    # North view needs transposition of lines and columns
    visible_from_n = [visible_from_left(trees) for trees in zip(*forest)]
    visible_from_n = list(zip(*visible_from_n))  # transpose result back

    # South view is reversed and transposed
    visible_from_s = [list(reversed(visible_from_left(reversed(trees)))) for trees in zip(*forest)]
    visible_from_s = list(zip(*visible_from_s))  # transpose result back

    visible = combine(visible_from_w, visible_from_e, operator.or_)
    visible = combine(visible, visible_from_n, operator.or_)
    visible = combine(visible, visible_from_s, operator.or_)
    return visible


def line_scenic_scores(trees):
    scores = [0]
    size = len(trees)
    trees = list(trees)
    for score_tree_index in range(1, size-1):
        score_tree = trees[score_tree_index]
        score_left = score_right = 0
        # scan to left
        for i in range(score_tree_index-1, -1, -1):
            score_left += 1
            if trees[i] >= score_tree:
                break
        # scan to right
        for i in range(score_tree_index + 1, size):
            score_right += 1
            if trees[i] >= score_tree:
                break
        scores.append(score_left * score_right)
    scores.append(0)
    return scores


def scenic_scores(forest):
    line_scores = [[0] * len(forest[0])]  # first line has score 0 (no tree view to the north)
    line_scores.extend(line_scenic_scores(trees) for trees in forest[1:-1])
    line_scores.append(line_scores[0])  # last line has score 0 (no tree view to the south)

    col_scores = [[0] * len(forest)]  # first column has score 0 (no tree view to the north)
    col_scores.extend([line_scenic_scores(trees) for trees in islice(zip(*forest), 1, len(forest)-1)])
    col_scores.append(col_scores[0])
    col_scores = list(zip(*col_scores))  # transpose

    scores = combine(line_scores, col_scores, operator.mul)
    return scores


def main(filename, testing=False, expected1=None, expected2=None):
    print(f'--------- {filename}')

    with open(filename) as f:
        forest = f.read().splitlines()

    result1 = sum(map(sum, visible_trees(forest)))
    print(f"Part 1: number of visible trees is {result1}")
    if testing and expected1 is not None:
        assert result1 == expected1

    scores = scenic_scores(forest)
    result2 = max(map(max, scores))
    print(f"Part 2: maximum scenic score is {result2}")
    if testing and expected2 is not None:
        assert result2 == expected2


if __name__ == '__main__':
    main('test.txt', True, 21, 8)
    main('input.txt')
