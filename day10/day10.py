import operator

from itertools import accumulate, starmap

instruction_cycles = {'addx': 2, 'noop': 1}


def run_program(program_lines, register_initial_value=1):
    cycle_consumption = list()
    register_add = list()
    for line in program_lines:
        instruction, value = (line + ' 0').split()[:2]
        register_add.append(int(value))
        cycle_consumption.append(instruction_cycles[instruction])

    register_values = accumulate(register_add, operator.add, initial=register_initial_value)
    cycle_for_value = accumulate(cycle_consumption, operator.add, initial=1)
    # Initial cycle_for_value is 1, because value is available at next cycle
    # For example, a first addx 15 instruction will cost 2 cycles, but its result will not be available until cycle 3

    return list(zip(cycle_for_value, register_values))


def signal_sampler(program_execution, sample_cycles):
    execution_data = dict(program_execution)
    for cycle in sample_cycles:
        yield cycle, execution_data[cycle] if cycle in execution_data else execution_data[cycle - 1]


def draw_crt(program_execution, width=40, height=6, lit_pixel='#', dark_pixel=' '):
    crt_lines = []
    crt_line = []
    signal = signal_sampler(program_execution, range(1, height * width + 1))  # start drawing at cycle 1
    crt_position = 0
    for cycle, sprite_position in signal:
        if -1 <= crt_position - sprite_position <= 1:
            crt_line.append(lit_pixel)
        else:
            crt_line.append(dark_pixel)
        crt_position += 1
        if crt_position == width:
            crt_position = 0
            crt_lines.append(''.join(crt_line))
            crt_line = []
    return '\n'.join(crt_lines)


def main(filename, testing=False, expected1=None, expected2=None):
    print(f'--------- {filename}')

    with open(filename) as f:
        program_lines = f.read().splitlines()

    program_execution = run_program(program_lines)
    cycles = range(20, 220 + 1, 40)  # 220 included, hence +1
    signal_strengths = starmap(operator.mul, signal_sampler(program_execution, cycles))

    result1 = sum(signal_strengths)
    print(f"Part 1: signal strength sample sum is {result1}")
    if testing and expected1 is not None:
        assert result1 == expected1

    result2 = draw_crt(program_execution, width=40, height=6,
                       lit_pixel='#' if testing else '\u2588',
                       dark_pixel='.' if testing else ' ')
    print(f"Part 2: CRT displays \n{result2}")
    if testing and expected2 is not None:
        assert result2 == expected2


if __name__ == '__main__':
    part_2_test_crt = """##..##..##..##..##..##..##..##..##..##..
###...###...###...###...###...###...###.
####....####....####....####....####....
#####.....#####.....#####.....#####.....
######......######......######......####
#######.......#######.......#######....."""

    main('test.txt', True, 13140, part_2_test_crt)
    main('input.txt')
