import operator

from itertools import accumulate

cycles = {'addx': 2, 'noop': 1}


def run_program(program_lines, register_initial_value=1):
    cycle_consumption = list()
    register_add = list()
    for line in program_lines:
        instruction, value = (line + ' 0').split()[:2]
        register_add.append(int(value))
        cycle_consumption.append(cycles[instruction])

    register_values = accumulate(register_add, operator.add, initial=register_initial_value)
    start_of_cycle = accumulate(cycle_consumption, operator.add, initial=1)
    # Initial start_of_cycle is 1, because value is available at next cycle
    # For example, a first addx 15 instruction will cost 2, but its result will not be available until cycle 3

    return list(zip(start_of_cycle, register_values))


def sample_signal_strength(program_execution, sample_cycles):
    execution_data = dict(program_execution)
    samples = [(sample_cycle,
                execution_data.get(sample_cycle) or execution_data.get(sample_cycle-1))
               for sample_cycle in sample_cycles]
    return samples


def solve_problem(filename, expected1=None, expected2=None):
    print(f'--------- {filename}')

    with open(filename) as f:
        program_lines = f.read().splitlines()

    program_execution = run_program(program_lines)
    signal_samples = sample_signal_strength(program_execution, range(20, 220+1, 40))  # 220 included, hence +1
    signal_strengths = [cycle * value for cycle, value in signal_samples]

    result1 = sum(signal_strengths)
    print(f"Part 1: signal strength sample sum is {result1}")
    if expected1 is not None:
        assert result1 == expected1

    result2 = 0
    print(f"Part 2: {result2}")
    if expected2 is not None:
        assert result2 == expected2


def main():
    solve_problem('test.txt', 13140)
    solve_problem('input.txt', 10760)


if __name__ == '__main__':
    main()
