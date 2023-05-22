use itertools::Itertools;
use std::{
    collections::HashMap,
    fs,
    hash::{Hash, Hasher},
    ops::{Add, Sub},
};

#[derive(Debug, Copy, Clone, PartialEq, Default, Eq)]
pub struct Point {
    pub x: i32,
    pub y: i32,
}

impl Hash for Point {
    fn hash<H: Hasher>(&self, state: &mut H) {
        (self.x, self.y).hash(state);
    }
}

impl Add for Point {
    type Output = Self;
    fn add(self, other: Self) -> Self {
        Self {
            x: self.x + other.x,
            y: self.y + other.y,
        }
    }
}

impl Sub for Point {
    type Output = Self;
    fn sub(self, other: Self) -> Self {
        Self {
            x: self.x - other.x,
            y: self.y - other.y,
        }
    }
}

pub enum Direction {
    Up,
    UpRight,
    Right,
    DownRight,
    Down,
    DownLeft,
    Left,
    Upleft,
}

impl Direction {
    fn value(&self) -> Point {
        match *self {
            Direction::Up => return Point { x: 0, y: -1 },
            Direction::UpRight => return Point { x: 1, y: -1 },
            Direction::Right => return Point { x: 1, y: 0 },
            Direction::Down => return Point { x: 0, y: 1 },
            Direction::DownRight => return Point { x: 1, y: 1 },
            Direction::Left => return Point { x: -1, y: 0 },
            Direction::DownLeft => return Point { x: -1, y: 1 },
            Direction::Upleft => return Point { x: -1, y: -1 },
        }
    }
}

const FALLPATH: [Direction; 3] = [Direction::Down, Direction::DownLeft, Direction::DownRight];

#[derive(PartialEq, Debug)]
enum Element {
    Rock,
    Sand,
}

type MapType = HashMap<Point, Element>;

#[derive(Debug)]
struct Cave {
    map: MapType,
    ymax: i32,
    start: Point,
}

impl Cave {
    fn parse(data: &String) -> Self {
        let mut map: MapType = HashMap::new();
        let mut ymax = i32::MIN;
        for line in data.trim().lines() {
            for (start, end) in line.split("->").tuple_windows() {
                let mut first = start
                    .split(",")
                    .into_iter()
                    .map(|x| x.trim().parse::<i32>().unwrap());
                let a = first.next().unwrap();
                let b = first.next().unwrap();
                let mut second = end
                    .split(",")
                    .into_iter()
                    .map(|x| x.trim().parse::<i32>().unwrap());
                let c = second.next().unwrap();
                let d = second.next().unwrap();
                if a == c {
                    let small = b.min(d);
                    let big = b.max(d);
                    for i in small..big + 1 {
                        map.insert(Point { x: a, y: i }, Element::Rock);
                        ymax = i.max(ymax);
                    }
                } else if b == d {
                    let small = a.min(c);
                    let big = a.max(c);
                    for i in small..big + 1 {
                        map.insert(Point { x: i, y: b }, Element::Rock);
                        ymax = b.max(ymax);
                    }
                }
            }
        }
        Self {
            map,
            ymax,
            start: Point { x: 500, y: 0 },
        }
    }
}

fn find_resting_point_1(cave: &Cave, point: Point) -> Option<Point> {
    if point.y > cave.ymax {
        return None;
    }
    for vector in FALLPATH {
        let npoint = vector.value() + point;
        match cave.map.get(&npoint) {
            None => {
                return find_resting_point_1(&cave, npoint);
            }
            Some(Element::Rock) | Some(Element::Sand) => {
                // this is fine
            }
        }
    }
    return Some(point);
}

fn step_until_finished_1(cave: &mut Cave) {
    let start = cave.start.clone();
    while let Some(point) = find_resting_point_1(&cave, start) {
        cave.map.insert(point, Element::Sand);
        if point == start {
            break;
        }
    }
}

fn find_resting_point_2(cave: &Cave, point: Point) -> Option<Point> {
    if point.y == cave.ymax + 1 {
        return Some(point);
    }
    for vector in FALLPATH {
        let npoint = vector.value() + point;
        match cave.map.get(&npoint) {
            None => {
                return find_resting_point_2(&cave, npoint);
            }
            Some(Element::Rock) | Some(Element::Sand) => {
                // this is fine
            }
        }
    }
    return Some(point);
}

fn step_until_finished_2(cave: &mut Cave) {
    let start = cave.start.clone();
    while let Some(point) = find_resting_point_2(&cave, start) {
        cave.map.insert(point, Element::Sand);
        if point == start {
            break;
        }
    }
}

fn part1() -> usize {
    let data = get_data();
    let mut cave = Cave::parse(&data);
    step_until_finished_1(&mut cave);
    let count = cave
        .map
        .values()
        .filter(|x| return x == &&Element::Sand)
        .count();
    return count;
}

fn part2() -> usize {
    let data = get_data();
    let mut cave = Cave::parse(&data);
    step_until_finished_2(&mut cave);
    let count = cave
        .map
        .values()
        .filter(|x| return x == &&Element::Sand)
        .count();
    return count;
}

fn get_data() -> String {
    return fs::read_to_string("../data/day14.txt").unwrap();
}

fn main() {
    let p1 = part1();
    println!("part 1: {}", p1);
    let p2 = part2();
    println!("part 2: {}", p2);
}
