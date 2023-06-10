use std::{
    fs,
    hash::{Hash, Hasher},
    ops::{Add, Sub}, collections::{HashSet, HashMap},
};

#[derive(Debug, Copy, Clone, PartialEq, Default, Eq)]
pub struct Point {
    pub x: i64,
    pub y: i64,
    pub z: i64,
}

impl Point {
    fn new(x: i64, y: i64, z: i64) -> Self{
        return Self {x, y, z}
    }
    fn get_adj(&self) -> Vec<Self>{
        vec![
            Self::new(self.x + 1, self.y, self.z),
            Self::new(self.x - 1, self.y, self.z),
            Self::new(self.x, self.y + 1, self.z),
            Self::new(self.x, self.y - 1, self.z),
            Self::new(self.x, self.y, self.z + 1),
            Self::new(self.x, self.y, self.z - 1),
        ]
    }
}

impl Hash for Point {
    fn hash<H: Hasher>(&self, state: &mut H) {
        (self.x, self.y, self.z).hash(state);
    }
}

impl Add for Point {
    type Output = Self;
    fn add(self, other: Self) -> Self {
        Self {
            x: self.x + other.x,
            y: self.y + other.y,
            z: self.z + other.z,
        }
    }
}

impl Sub for Point {
    type Output = Self;
    fn sub(self, other: Self) -> Self {
        Self {
            x: self.x - other.x,
            y: self.y - other.y,
            z: self.z - other.z,
        }
    }
}

#[derive(Debug)]
struct Space {
    points: HashSet<Point>,
    x: HashMap<(i64, i64), Vec<Point>>,
    y: HashMap<(i64, i64), Vec<Point>>,
    z: HashMap<(i64, i64), Vec<Point>>,
    min_x: i64,
    max_x: i64,
    min_y: i64,
    max_y: i64,
    min_z: i64,
    max_z: i64,
    bubbles: HashSet<Point>,
}

impl From<String> for Space {
    fn from(data: String) -> Self {
        let mut cubes: HashSet<Point> = HashSet::new();
        let mut x: HashMap<(i64, i64), Vec<Point>> = HashMap::new();
        let mut y: HashMap<(i64, i64), Vec<Point>> = HashMap::new();
        let mut z: HashMap<(i64, i64), Vec<Point>> = HashMap::new();
        let mut min_x = i64::MAX;
        let mut max_x = i64::MIN;
        let mut min_y = i64::MAX;
        let mut max_y = i64::MIN;
        let mut min_z = i64::MAX;
        let mut max_z = i64::MIN;
        for line in data.trim().lines() {
            let mut parts = line.split(",").into_iter().map(|x| x.parse::<i64>().unwrap());
            let a = parts.next().unwrap();
            let b = parts.next().unwrap();
            let c = parts.next().unwrap();
            let point = Point::new(a, b, c);
            cubes.insert(point.clone());
            // x.entry((point.y, point.z)).and_modify(|val| val.push(point.clone())).or_insert(vec![point.clone()]);
            x.entry((point.y, point.z)).or_insert(vec![]).push(point.clone());
            y.entry((point.x, point.z)).or_insert(vec![]).push(point.clone());
            z.entry((point.x, point.y)).or_insert(vec![]).push(point.clone());
            min_x = min_x.min(point.x);
            max_x = max_x.max(point.x);
            min_y = min_y.min(point.y);
            max_y = max_y.max(point.y);
            min_z = min_z.min(point.z);
            max_z = max_z.max(point.z);
        }
        for (_, val) in x.iter_mut() {
            val.sort_by_key(|entry| entry.x);
        }
        for (_, val) in y.iter_mut() {
            val.sort_by_key(|entry| entry.y);
        }
        for (_, val) in z.iter_mut() {
            val.sort_by_key(|entry| entry.z);
        }
        return Self {
            points: cubes,
            x,
            y,
            z,
            min_x,
            max_x,
            min_y,
            max_y,
            min_z,
            max_z,
            bubbles: HashSet::new(),
        }
    }
}

impl Space {
    fn surface_area(&self) -> i64 {
        let mut count = 0;
        for point in self.points.iter() {
            for adj in point.get_adj() {
                if !self.points.contains(&adj) {
                    count += 1;
                }
            }
        }
        return count;
    }
    fn has_cube_all_sides(&self, point: &Point) -> bool {
        if let Some(x_cubes) = self.x.get(&(point.y, point.z)) {
            let lt = x_cubes.first().unwrap();
            let gt = x_cubes.last().unwrap();
            if lt.x >= point.x || gt.x <= point.x {
                return false
            }
        }
        if let Some(y_cubes) = self.y.get(&(point.x, point.z)) {
            let lt = y_cubes.first().unwrap();
            let gt = y_cubes.last().unwrap();
            if lt.y >= point.y || gt.y <= point.y {
                return false
            }
        }
        if let Some(z_cubes) = self.z.get(&(point.x, point.y)) {
            let lt = z_cubes.first().unwrap();
            let gt = z_cubes.last().unwrap();
            if lt.z >= point.z || gt.z <= point.z {
                return false
            }
        }
        return true
    }
    fn external_surface_area(&mut self) -> i64 {
        let mut count = 0;
        for point in self.points.iter() {
            for adj in point.get_adj() {
                if !self.points.contains(&adj) {
                    if self.has_cube_all_sides(&adj) {
                        let flooded = self.flood(&adj);
                        if flooded.is_empty() {
                            count += 1;
                        }
                        for other in flooded {
                            self.bubbles.insert(other);
                        }
                    } else {
                        count += 1;
                    }
                }
            }
        }
        return count;
    }
    fn flood(&self, point: &Point) -> HashSet<Point> {
        let mut stack = vec![point.clone()];
        let mut flooded: HashSet<Point> = HashSet::new();
        while let Some(item) = stack.pop() {
            if self.bubbles.contains(&item) {
                return self.bubbles.clone()
            }
            if item.x < self.min_x || item.x > self.max_x {
                return HashSet::new();
            } else if item.y < self.min_y || item.y > self.max_y {
                return HashSet::new();
            } else if item.z < self.min_z || item.z > self.max_z {
                return HashSet::new();
            }
            flooded.insert(item.clone());
            for other in item.get_adj() {
                if !self.points.contains(&other) && !flooded.contains(&other) {
                    stack.push(other.clone());
                }
            }
        }
        return flooded
    }
}



fn part1() -> i64 {
    let data = get_data().trim().to_string();
    let space = Space::from(data);
    return space.surface_area();
}

fn part2() -> i64 {
    let data = get_data().trim().to_string();
    let mut space = Space::from(data);
    return space.external_surface_area();
}

fn get_data() -> String {
    return fs::read_to_string("../data/day18.txt").unwrap();
}

fn main() {
    let p1 = part1();
    println!("part 1: {}", p1);
    let p2 = part2();
    println!("part 2: {}", p2);
}
