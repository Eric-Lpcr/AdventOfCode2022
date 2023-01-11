from collections import namedtuple, deque
from itertools import chain

from operator import attrgetter

Coordinate = namedtuple('Coordinate', 'x, y')
SensorBeaconPair = namedtuple('SensorBeaconPair', 'sensor, beacon, dist')


def manhattan(coord1, coord2):
    return abs(coord2.x - coord1.x) + abs(coord2.y - coord1.y)


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
    sensor = Coordinate(xs, ys)
    beacon = Coordinate(xb, yb)
    return SensorBeaconPair(sensor, beacon, manhattan(beacon, sensor))


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


def find_distress_beacon(sensors_data, limit):
    # The sole distress beacon has to be surrounded by diamonds from other sensors.
    # For each sensor, get the points on the border, and check for each whether
    # they're in range of any sensors, return if one is found outside all the ranges.
    for sensor, _, dist in sensors_data:
        for a in range(0, dist + 1):
            b = dist + 1 - a
            for dx, dy in [(a, b), (a, -b), (-a, b), (-a, -b)]:
                p = Coordinate(sensor.x + dx, sensor.y + dy)  # points just outside the diamond
                if 0 <= p.x <= limit and 0 <= p.y <= limit:
                    if all(manhattan(p, s) > d for s, _, d in sensors_data):
                        return p
    return None


def main(filename, testing=False, expected1=None, expected2=None):
    print(f'--------- {filename}')

    with open(filename) as f:
        sensors_data = [decode_sensor(sensor_info) for sensor_info in f.readlines()]

    row_of_interest = 10 if testing else 2_000_000
    result1 = scan_row(sensors_data, row_of_interest)
    print(f"Part 1: positions where a beacon cannot be present are {result1}")
    if testing and expected1 is not None:
        assert result1 == expected1

    limit = 20 if testing else 4_000_000
    distress_beacon = find_distress_beacon(sensors_data, limit)
    result2 = distress_beacon.x * 4_000_000 + distress_beacon.y
    print(f"Part 2: beacon tuning frequency is {result2}")
    if testing and expected2 is not None:
        assert result2 == expected2


if __name__ == '__main__':
    main('test.txt', True, 26, 56000011)
    main('input.txt')
