use std::{
    collections::{HashMap, VecDeque},
    fs,
    hash::{Hash, Hasher},
    ops::{Add, Sub},
};

enum Direction {
    Up,
    Down,
    Left,
    Right,
}

impl Direction {
    fn value(&self) -> Point {
        match *self {
            Direction::Up => return Point { x: 0, y: 1 },
            Direction::Down => return Point { x: 0, y: -1 },
            Direction::Right => return Point { x: 1, y: 0 },
            Direction::Left => return Point { x: -1, y: 0 },
        }
    }
}

const DIR_LIST: [Direction; 4] = [
    Direction::Up,
    Direction::Down,
    Direction::Left,
    Direction::Right,
];

#[derive(Debug, Copy, Clone, PartialEq, Default, Eq)]
struct Point {
    x: i16,
    y: i16,
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

type Map = HashMap<Point, i16>;

#[derive(Debug)]
struct Hill {
    map: Map,
    start: Point,
    end: Point,
}

impl From<String> for Hill {
    fn from(value: String) -> Self {
        let ascii = get_ascii_map();
        let mut map: Map = HashMap::new();
        let mut start = Point::default();
        let mut end = start.clone();
        for (y, row) in value.lines().enumerate() {
            for (x, ch) in row.chars().enumerate() {
                let point = Point {
                    x: x as i16,
                    y: y as i16,
                };
                if ch == 'S' {
                    start = point.clone();
                } else if ch == 'E' {
                    end = point.clone();
                }
                map.insert(point, ascii.get(&ch.to_string()).unwrap().clone());
            }
        }
        return Self { map, start, end };
    }
}

impl Hill {
    fn find_end(&self, start: Point, backwards: bool) -> HashMap<Point, i16> {
        let mut queue: VecDeque<(Point, i16)> = VecDeque::new();
        queue.push_back((start.clone(), 0));
        let mut visited: HashMap<Point, i16> = HashMap::new();
        while let Some((point, dist)) = queue.pop_front() {
            if let Some(found) = visited.get(&point) {
                if &dist >= found {
                    continue;
                }
            } else {
                visited.insert(point.clone(), dist.clone());
            }
            let height = self.map.get(&point).unwrap().clone();
            for d in DIR_LIST.iter() {
                let other = point + d.value();
                let other_val_opt = self.map.get(&other);
                if other_val_opt == None {
                    continue;
                }
                let other_height = other_val_opt.unwrap().clone();
                if backwards {
                    if other_height >= height - 1 {
                        queue.push_back((other, dist + 1));
                    }
                } else {
                    if other_height <= height + 1 {
                        queue.push_back((other, dist + 1));
                    }
                }
            }
        }
        return visited;
    }
    fn get_all_a(&self) -> Vec<Point> {
        return self.map.iter().filter_map(|(x, y)| {
            if *y == 0 {
                return Some(x.clone());
            }
            return None;
        }).collect::<Vec<_>>();
    }
    fn find_min_dist(&self, distances: &HashMap<Point, i16>) -> i16 {
        return self.get_all_a().iter().map(|point| {
            if let Some(dist) = distances.get(&point) {
                return dist.clone()
            }
            return i16::MAX;
        }).min().unwrap();
    }
}

fn get_ascii_map() -> HashMap<String, i16> {
    let ascii = "abcdefghijklmnopqrstuvwxyz";
    let mut map: HashMap<String, i16> = HashMap::new();
    for (i, ch) in ascii.chars().enumerate() {
        map.insert(ch.to_string(), i as i16);
    }
    let a = map.get(&"a".to_string()).unwrap().clone();
    let z = map.get(&"z".to_string()).unwrap().clone();
    map.insert("S".to_string(), a);
    map.insert("E".to_string(), z);
    return map;
}

fn get_data() -> String {
    let data = fs::read_to_string("../data/day12.txt").unwrap();
    return data;
}

fn part1(start: &Point, distances: &HashMap<Point, i16>) -> i16 {
    return distances.get(start).unwrap().clone();
}

fn part2(map: &Hill, distances: &HashMap<Point, i16>) -> i16 {
    return map.find_min_dist(distances);
}

fn main() {
    let data = get_data();
    let map = Hill::from(data.clone());
    let distances = map.find_end(map.end, true);
    let p1 = part1(&map.start, &distances);
    println!("Part 1: {}", p1);
    let p2 = part2(&map, &distances);
    println!("Part 2: {}", p2);
}
