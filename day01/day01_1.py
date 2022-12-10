
def main(filename, testing=False, expected1=None, expected2=None):
    print(f'--------- {filename}')

    with open(filename) as f:
        input_data = [list(map(int, elf_lines.split())) for elf_lines in f.read().split('\n\n')]

    elves_calories = map(sum, input_data)

    result1 = max(elves_calories)
    print(f"Part 1: maximum elf calories is {result1}")
    if testing and expected1 is not None:
        assert result1 == expected1

    result2 = None
    print(f"Part 2: {result2}")

    if testing and expected2 is not None:
        assert result2 == expected2


if __name__ == '__main__':
    main('test.txt', True, 24000, None)
    main('input.txt')
