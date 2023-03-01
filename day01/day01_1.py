
def solve_problem(filename, expected1=None, expected2=None):
    print(f'--------- {filename}')

    with open(filename) as f:
        input_data = [list(map(int, elf_lines.split())) for elf_lines in f.read().split('\n\n')]

    elves_calories = map(sum, input_data)

    result1 = max(elves_calories)
    print(f"Part 1: maximum elf calories is {result1}")
    if expected1 is not None:
        assert result1 == expected1

    result2 = None
    print(f"Part 2: {result2}")

    if expected2 is not None:
        assert result2 == expected2


def main():
    solve_problem('test.txt', 24000)
    solve_problem('input.txt', 68787)


if __name__ == '__main__':
    main()
