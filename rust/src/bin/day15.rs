use regex::Regex;
use std::{
    collections::HashSet,
    fs,
    hash::{Hash, Hasher},
    ops::{Add, Sub},
};

#[derive(Debug, Copy, Clone, PartialEq, Default, Eq)]
pub struct Point {
    pub x: i64,
    pub y: i64,
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

#[derive(Clone)]
struct Sensor {
    pos: Point,
    beacon_distance: i64,
    xmin: i64,
    xmax: i64,
}

fn m_dist(p1: &Point, p2: &Point) -> i64 {
    let p3 = *p1 - *p2;
    return p3.x.abs() + p3.y.abs()
}

impl Sensor {
    fn new(pos: Point, beacon: Point) -> Self {
        let beacon_distance = m_dist(&pos, &beacon);
        let xmin = pos.x - beacon_distance;
        let xmax = pos.x + beacon_distance;
        return Self {
            pos,
            beacon_distance,
            xmin,
            xmax,
        }
    }
    fn contains(&self, point: &Point) -> bool {
        return m_dist(&self.pos, point) <= self.beacon_distance;
    }
    fn range_for_row(&self, y: i64) -> (i64, i64) {
        let dy = (y - self.pos.y).abs();
        let abs_x = (self.beacon_distance - dy).abs();
        return (self.pos.x - abs_x, self.pos.x + abs_x)
    }
}

struct Map {
    sensors: Vec<Sensor>,
    beacons: HashSet<Point>,
    xmin: i64,
    xmax: i64
}

impl From<&String> for Map {
    fn from(value: &String) -> Self {
        let mut sensors: Vec<Sensor> = vec![];
        let mut beacons: HashSet<Point> = HashSet::new();
        let re = Regex::new(r".*?(-?\d+).*?(-?\d+).*?(-?\d+).*?(-?\d+)").unwrap();
        let mut xmin = i64::MAX;
        let mut xmax = i64::MIN;
        for m in re.captures_iter(value.trim()) {
            let x = m.get(1).unwrap().as_str().parse::<i64>().unwrap();
            let y = m.get(2).unwrap().as_str().parse::<i64>().unwrap();
            let bx = m.get(3).unwrap().as_str().parse::<i64>().unwrap();
            let by = m.get(4).unwrap().as_str().parse::<i64>().unwrap();
            let beacon = Point {x: bx, y: by};
            let sensor = Sensor::new(Point {x, y}, beacon.clone());
            xmin = sensor.xmin.min(xmin);
            xmax = sensor.xmax.max(xmax);
            sensors.push(sensor);
            beacons.insert(beacon);
        }
        return Self {
            sensors,
            beacons,
            xmin,
            xmax,
        }
    }
}


impl Map {
    fn point_in_range(&self, point: &Point) -> Option<Sensor> {
        for sensor in self.sensors.iter() {
            if sensor.contains(&point) {
                if !self.beacons.contains(&point) {
                    return Some(sensor.clone())
                }
            }
        }
        return None
    }
    fn find_empty_spaces(&self, y: i64) -> i64 {
        let mut count = 0i64;
        for x in self.xmin..self.xmax+1 {
            if self.point_in_range(&Point {x, y}).is_some() {
                count += 1;
            }
        }
        return count
    }
    fn find_empty_space(&self, max_val: i64) -> Point {
        let mut x = 0i64;
        let mut y = 0i64;
        while y < max_val + 1 {
            if x > max_val {
                y += 1;
                x = 0;
            }
            let point = Point {x, y};
            match self.point_in_range(&point) {
                Some(sensor) => {
                    let (_, nx) = sensor.range_for_row(point.y);
                    x = nx + 1;
                }
                None => {
                    return point
                }
            }
        }
        panic!("Shouldn't get here.")
    }
}


fn solve() {
    let data = get_data();
    let smap = Map::from(&data);
    let count = smap.find_empty_spaces(2000000);
    println!("Part 1: {}", count);
    let pos = smap.find_empty_space(4000000);
    let p2 = pos.x * 4000000 + pos.y;
    println!("Part 2: {}", p2);
}

fn get_data() -> String {
    return fs::read_to_string("../data/day15.txt").unwrap();
}

fn main() {
    solve();
}
