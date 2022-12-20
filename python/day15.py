from functools import cached_property
from pathlib import Path
from dataclasses import dataclass
import re

file = Path(__file__).parent.parent / "data" / "day15.txt"
raw = file.read_text().strip()

Point = tuple[int, int]


@dataclass
class Sensor:
    pos: Point
    beacon: Point

    @cached_property
    def beacon_distance(self):
        return self.m_dist(self.beacon)

    def contains(self, point: Point):
        return self.m_dist(point) <= self.beacon_distance

    def m_dist(self, point: Point):
        dx, dy = (abs(a - b) for a, b in zip(self.pos, point))
        return dx + dy

    def range_for_row(self, y: int):
        dist = self.beacon_distance
        dy = abs(y - self.pos[1])
        abs_x = dist - dy
        return self.pos[0] - abs_x, self.pos[0] + abs_x

    @cached_property
    def xmin(self):
        return self.pos[0] - self.beacon_distance

    @cached_property
    def xmax(self):
        return self.pos[0] + self.beacon_distance


@dataclass
class SensorMap:
    sensors: list[Sensor]
    beacons: set[Point]
    xmin: int
    xmax: int

    @classmethod
    def parse(cls, data: str):
        sensors = []
        beacons = set()
        xmin = float('inf')
        xmax = -float('inf')
        for row in re.findall(r'.*?(-?\d+).*?(-?\d+).*?(-?\d+).*?(-?\d+)', data):
            x, y, bx, by = map(int, row)
            sensor = Sensor(pos=(x, y), beacon=(bx, by))
            sensors.append(sensor)
            beacons.add((bx, by))
            xmin = min(sensor.xmin, xmin)
            xmax = max(sensor.xmax, xmax)
        return cls(sensors=sensors, beacons=beacons, xmin=int(xmin), xmax=int(xmax))

    def point_in_range(self, point: Point):
        for sensor in self.sensors:
            if sensor.contains(point):
                if point not in self.beacons:
                    return sensor
        return False


    def find_empty_spaces(self, y: int):
        count = 0
        for x in range(self.xmin, self.xmax + 1):
            if self.point_in_range((x, y)):
                count += 1
        return count

    def find_empty_space(self, max_val: int):
        x = y = 0
        while y < max_val + 1:
            if x > max_val:
                y += 1
                x = 0
            sensor = self.point_in_range((x, y))
            if not sensor:
                return (x, y)
            _, x = sensor.range_for_row(y)
            x += 1
        raise Exception


smap = SensorMap.parse(raw)


count = smap.find_empty_spaces(2000000)
print(count)

pos = smap.find_empty_space(4000000)
p2 = pos[0] * 4000000 + pos[1]
print(p2)
