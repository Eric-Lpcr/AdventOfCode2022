
def solve_problem(filename, expected1=None, expected2=None):
    print(f'--------- {filename}')

    with open(filename) as f:
        input_data = [list(map(int, elf_lines.split())) for elf_lines in f.read().split('\n\n')]

    elves_calories = list(map(sum, input_data))

    result1 = max(elves_calories)
    print(f"Part 1: maximum elf calories is {result1}")
    if expected1 is not None:
        assert result1 == expected1

    result2 = sum(sorted(elves_calories)[-3:])
    print(f"Part 2: sum of top three maximum elf calories is {result2}")

    if expected2 is not None:
        assert result2 == expected2


def main():
    solve_problem('test.txt', 24000, 45000)
    solve_problem('input.txt', 68787, 198041)


if __name__ == '__main__':
    main()
