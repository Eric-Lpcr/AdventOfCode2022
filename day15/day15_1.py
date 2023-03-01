from collections import namedtuple, deque
from itertools import chain

from operator import attrgetter

Coordinate = namedtuple('Coordinate', 'x, y')
SensorBeaconPair = namedtuple('SensorBeaconPair', 'sensor, beacon, dist')


class InclusiveRange:
    def __init__(self, begin, end):
        self.begin = min(begin, end)
        self.end = max(begin, end)

    def __contains__(self, item):
        if isinstance(item, InclusiveRange):
            return item.begin in self and item.end in self
        else:
            return self.begin <= item <= self.end

    def overlaps(self, another_range):
        return another_range.begin in self or self.begin in another_range

    def size(self):
        return self.end - self.begin + 1

    def __str__(self):
        return f'[{self.begin}, {self.end}]'

    def __repr__(self):
        return str(self)


def decode_sensor(sensor_info):
    xs, ys, xb, yb = map(int,
                         sensor_info.replace('Sensor at x=', '')
                         .replace(', y=', ' ')
                         .replace(': closest beacon is at x=', ' ')
                         .split())
    return SensorBeaconPair(Coordinate(xs, ys), Coordinate(xb, yb), abs(xb - xs) + abs(yb - ys))


def scan_row(sensors_data, row_of_interest):
    ranges = []
    for sensor, beacon, dist in sensors_data:
        half_width = dist - abs(row_of_interest - sensor.y)
        if half_width >= 0:  # diamond intersects row of interest
            ranges.append(InclusiveRange(sensor.x - half_width, sensor.x + half_width))

    combined_ranges = deque()  # need to resolve intersections to count them only once
    for r in sorted(ranges, key=attrgetter('begin')):
        previous_r = combined_ranges.pop() if len(combined_ranges) > 0 else r
        if r.overlaps(previous_r):  # combine
            combined_ranges.append(InclusiveRange(min(previous_r.begin, r.begin), max(previous_r.end, r.end)))
        else:
            combined_ranges.append(previous_r)
            combined_ranges.append(r)

    ranges_size = sum(r.size() for r in combined_ranges)

    # count objects (sensors, beacons) on row of interest
    # need a set because a beacon can be detected by more than one sensor
    objects = set(chain(*((s, b) for s, b, _ in sensors_data)))
    object_count = sum(any(obj.x in r for r in ranges) for obj in objects if obj.y == row_of_interest)

    return ranges_size - object_count


def solve_problem(filename, expected1=None, expected2=None, testing=False):
    print(f'--------- {filename}')

    with open(filename) as f:
        sensors_data = [decode_sensor(sensor_info) for sensor_info in f.readlines()]

    row_of_interest = 10 if testing else 2_000_000
    result1 = scan_row(sensors_data, row_of_interest)
    print(f"Part 1: positions where a beacon cannot be present are {result1}")
    if expected1 is not None:
        assert result1 == expected1

    result2 = 0
    print(f"Part 2: {result2}")
    if expected2 is not None:
        assert result2 == expected2


def main():
    solve_problem('test.txt', 26, testing=True)
    solve_problem('input.txt', 5240818)


if __name__ == '__main__':
    main()
