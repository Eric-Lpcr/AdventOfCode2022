

def visible_trees(trees):
    highest_tree = ''
    visible = []
    for i, tree in enumerate(trees):
        if tree > highest_tree:
            visible.append(True)
            highest_tree = tree
        else:
            visible.append(False)
    return visible


def combine_or(visible1, visible2):
    visible = []
    for line1, line2 in zip(visible1, visible2):
        visible.append([b1 or b2 for b1, b2 in zip(line1, line2)])
    return visible


def count_visible_trees(forest):
    visible_from_w = [visible_trees(trees) for trees in forest]
    visible_from_e = [list(reversed(visible_trees(reversed(trees)))) for trees in forest]
    visible_from_n = list(zip(*[visible_trees(trees) for trees in zip(*forest)]))
    visible_from_s = list(zip(*[list(reversed(visible_trees(reversed(trees)))) for trees in zip(*forest)]))

    visible = combine_or(visible_from_w, visible_from_e)
    visible = combine_or(visible, visible_from_n)
    visible = combine_or(visible, visible_from_s)

    return sum(map(sum, visible))


def solve_problem(filename, expected1=None, expected2=None):
    print(f'--------- {filename}')

    with open(filename) as f:
        forest = f.read().splitlines()

    result1 = count_visible_trees(forest)
    print(f"Part 1: number of visible trees is {result1}")
    if expected1 is not None:
        assert result1 == expected1

    result2 = 0
    print(f"Part 2:  {result2}")
    if expected2 is not None:
        assert result2 == expected2


def main():
    solve_problem('test.txt', 21)
    solve_problem('input.txt', 1825)


if __name__ == '__main__':
    main()
