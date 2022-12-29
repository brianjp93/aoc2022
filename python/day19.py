from pathlib import Path
from dataclasses import dataclass
import re
from typing import NotRequired, TypedDict
from math import prod

file = Path(__file__).parent.parent / "data" / "day19.txt"
raw = file.read_text().strip()


class Resources(TypedDict):
    ore: NotRequired[int]
    clay: NotRequired[int]
    obsidian: NotRequired[int]
    geode: NotRequired[int]


class BluePrint(TypedDict):
    ore: Resources
    clay: Resources
    obsidian: Resources
    geode: Resources


class Robots(TypedDict):
    ore: int
    clay: int
    obsidian: int
    geode: int


@dataclass(frozen=True)
class Item:
    minute: int
    robots: Robots
    resources: Resources

    @staticmethod
    def collect_resources(resources: Resources, robots: Robots):
        ret = resources.copy()
        for robot, count in robots.items():
            ret[robot] += count
        return ret

    @staticmethod
    def max_possible(
        geode_bots: int, minutes_left: int, bp: BluePrint, resources: Resources
    ):
        can_build = True
        resources = resources.copy()
        offset = 0
        for res, count in bp["geode"].items():
            if count > resources[res]:
                can_build = False
        if not can_build:
            minutes_left -= 1
            offset = geode_bots
        n1 = geode_bots
        n2 = minutes_left + geode_bots
        n2_total = int(n2 * (n2 - 1) / 2)
        n1_total = int(n1 * (n1 - 1) / 2)
        return n2_total - n1_total + resources.get("geode", 0) + offset

    def buildable(self, bp: BluePrint):
        buildable: dict[str, "Item"] = {}
        for robot in bp:
            costs: Resources = bp[robot]
            resources = self.resources.copy()
            can_build = True
            for resource in costs:
                cost: int = costs[resource]
                resources[resource] -= cost
                if resources[resource] < 0:
                    can_build = False
                    break
            if can_build:
                next_resources = self.collect_resources(resources, self.robots)
                robots = self.robots.copy()
                robots[robot] += 1
                item = self.__class__(self.minute + 1, robots, next_resources)
                buildable[robot] = item

        next_resources = self.collect_resources(self.resources, self.robots)
        yield self.__class__(self.minute + 1, self.robots.copy(), next_resources)
        yield from buildable.values()


@dataclass
class Factory:
    bp: BluePrint

    @staticmethod
    def init_robots() -> Robots:
        return {
            "ore": 1,
            "clay": 0,
            "obsidian": 0,
            "geode": 0,
        }

    def simulation(self, minutes=24):
        robots = self.init_robots()
        stack = [
            Item(
                minute=1,
                robots=robots,
                resources={
                    "ore": 0,
                    "clay": 0,
                    "obsidian": 0,
                    "geode": 0,
                },
            )
        ]
        top = 0
        seen = {}
        while stack:
            item = stack.pop()
            frozen = tuple(item.resources.values()), tuple(item.robots.values())
            if frozen in seen:
                if seen[frozen] <= item.minute:
                    continue
            seen[frozen] = item.minute
            max_possible = item.max_possible(
                item.robots["geode"], minutes + 1 - item.minute, self.bp, item.resources
            )
            if max_possible <= top:
                continue
            if item.minute == minutes + 1:
                if item.resources.get("geode", 0) > top:
                    top = item.resources.get("geode", 0)
                    print(f'{top=}')
                continue
            for buildable in item.buildable(self.bp):
                stack.append(buildable)
        return top


def parse(data: str):
    factories: list[Factory] = []
    for parts in re.findall(
        r"Blueprint \d+:.*?(\d+).*?(\d+).*?(\d+).*?(\d+).*?(\d+).*?(\d+)", data
    ):
        a, b, c, d, e, f = map(int, parts)
        bp: BluePrint = {
            "ore": {"ore": a},
            "clay": {"ore": b},
            "obsidian": {"ore": c, "clay": d},
            "geode": {"ore": e, "obsidian": f},
        }
        factory = Factory(bp=bp)
        factories.append(factory)
    return factories


def part1():
    factories = parse(raw)
    quality_levels = []
    for i, factory in enumerate(factories, start=1):
        out = factory.simulation()
        quality_levels.append(i * out)
    return sum(quality_levels)

def part2():
    factories = parse(raw)
    geodes = []
    for factory in factories[:3]:
        out = factory.simulation(minutes=32)
        geodes.append(out)
    return prod(geodes)

print(f'{part1()=}')
print(f'{part2()=}')
