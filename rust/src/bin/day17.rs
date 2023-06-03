use std::{
    fs,
    hash::{Hash, Hasher},
    ops::{Add, Sub}, collections::HashSet,
};

use itertools::Itertools;

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

enum BlockType {
    Flat,
    Plus,
    RevL,
    Line,
    Square,
}

impl BlockType {
    fn create(&self) -> Block {
        match self {
            Self::Flat => {
                return Block::flat();
            }
            Self::Plus => {
                return Block::plus();
            }
            Self::RevL => {
                return Block::rev_l();
            }
            Self::Line => {
                return Block::line();
            }
            Self::Square => {
                return Block::square();
            }
        }
    }
}

const ORDER: [BlockType; 5] = [
    BlockType::Flat,
    BlockType::Plus,
    BlockType::RevL,
    BlockType::Line,
    BlockType::Square,
];

#[derive(Clone)]
struct Block {
    map: Vec<Point>,
}

impl Block {
    fn shift(&mut self, vector: &Point) {
        for i in 0..self.map.len() {
            self.map[i] = self.map[i] + *vector;
        }
    }
    fn bottom(&self) -> &Point {
        let mut check = &self.map[0];
        for point in self.map.iter() {
            if point.y < check.y {
                check = point;
            }
        }
        return check;
    }
    fn left(&self) -> &Point {
        let mut check = &self.map[0];
        for point in self.map.iter() {
            if point.x < check.x {
                check = point;
            }
        }
        return check;
    }
    fn right(&self) -> &Point {
        let mut check = &self.map[0];
        for point in self.map.iter() {
            if point.x > check.x {
                check = point;
            }
        }
        return check;
    }
    fn top(&self) -> &Point {
        let mut check = &self.map[0];
        for point in self.map.iter() {
            if point.y > check.y {
                check = point;
            }
        }
        return check;
    }
    fn flat() -> Self {
        return Self {
            map: vec![
                Point { x: 0, y: 0 },
                Point { x: 1, y: 0 },
                Point { x: 2, y: 0 },
                Point { x: 3, y: 0 },
            ],
        };
    }
    fn plus() -> Self {
        return Self {
            map: vec![
                Point { x: 1, y: 0 },
                Point { x: 0, y: 1 },
                Point { x: 1, y: 1 },
                Point { x: 2, y: 1 },
                Point { x: 1, y: 2 },
            ],
        };
    }
    fn rev_l() -> Self {
        return Self {
            map: vec![
                Point { x: 0, y: 0 },
                Point { x: 1, y: 0 },
                Point { x: 2, y: 0 },
                Point { x: 2, y: 1 },
                Point { x: 2, y: 2 },
            ],
        };
    }
    fn line() -> Self {
        return Self {
            map: vec![
                Point { x: 0, y: 0 },
                Point { x: 0, y: 1 },
                Point { x: 0, y: 2 },
                Point { x: 0, y: 3 },
            ],
        };
    }
    fn square() -> Self {
        return Self {
            map: vec![
                Point { x: 0, y: 0 },
                Point { x: 0, y: 1 },
                Point { x: 1, y: 0 },
                Point { x: 1, y: 1 },
            ],
        };
    }
}

#[derive(Debug)]
struct Chamber {
    map: HashSet<Point>,
    raw: Vec<char>,
}

impl Chamber {
    fn new(data: &Vec<char>) -> Self {
        return Self {
            map: HashSet::new(),
            raw: data.clone(),
        }
    }
    fn init_block(&self, block: &mut Block, top_y: &i64) {
        let left = block.left();
        let xpoint = Point {x: 2, y: left.y} - *left;
        let bottom = block.bottom();
        let ypoint = Point {x: bottom.x, y: top_y + 4} - *bottom;
        let movement = xpoint + ypoint;
        block.shift(&movement);
    }
    fn run_simulation(&mut self, rock_count: i64) -> i64 {
        let mut top_y = -1i64;
        let mut rocks = 0i64;
        let mut block_step = 0usize;
        let mut block: Option<Block> = None;
        let mut jet_step = 0usize;
        while rocks < rock_count {
            if block.is_none() {
                let mut block_obj = ORDER.get(block_step).unwrap().create();
                block_step = (block_step + 1) % ORDER.len();
                self.init_block(&mut block_obj, &top_y);
                block = Some(block_obj);
            }
            let shift = match self.raw[jet_step] {
                '>' => {
                    Direction::Right.value()
                }
                '<' => {
                    Direction::Left.value()
                }
                _ => panic!("Uh oh")
            };
            jet_step = (jet_step + 1) % self.raw.len();
            let block_obj = block.as_mut().unwrap();
            block_obj.shift(&shift);
            if self.is_collision(&block_obj) {
                block_obj.shift(&(Point {x: 0, y: 0} - shift));
            }
            block_obj.shift(&(Direction::Down.value()));
            if self.is_collision(&block_obj) {
                block_obj.shift(&(Direction::Up.value()));
                for point in block_obj.map.iter() {
                    self.map.insert(point.clone());
                }
                top_y = top_y.max(block_obj.top().y);
                block = None;
                rocks += 1;
            }
        }
        return top_y
    }
    fn get_big_rocks(&mut self, rock_count: i64) -> i64 {
        let mut top_y = -1;
        let mut rocks = 0;
        let mut block_step = 0;
        let mut block_opt: Option<Block> = None;
        let mut jet_step = 0;
        let mut last_height = 0;
        let mut last_rocks = 0;
        let mut cycle = 0;
        let mut dy_first = 0;
        let mut drock_first = 0;
        let mut offset_height = 0;
        let mut height_after_cycles = 0;
        let mut rocks_remaining: Option<i64> = None;
        let mut end_rock_count = 0;
        loop {
            if jet_step == 0 {
                let new_height = top_y + 1;
                let dy = new_height - last_height;
                let drocks = rocks - last_rocks;
                last_rocks = rocks;
                last_height = new_height;
                if cycle == 1 {
                    dy_first = dy;
                    drock_first = drocks;
                } else if cycle == 2 {
                    let dy_cycle = dy;
                    let drock_cycle = drocks;
                    let rocks_left = rock_count - drock_first;
                    let cycles_left = rocks_left / drock_cycle;
                    let rocks_after_cycles = (drock_cycle * cycles_left) + drock_first;
                    height_after_cycles = (dy_cycle * cycles_left) + dy_first;
                    rocks_remaining = Some(rock_count - rocks_after_cycles);
                    offset_height = new_height;
                    end_rock_count = 0;
                }
                cycle += 1;
            }
            if block_opt.is_none() {
                let mut block = ORDER.get(block_step).unwrap().create();
                block_step = (block_step + 1) % ORDER.len();
                self.init_block(&mut block, &top_y);
                block_opt = Some(block);
            }
            let shift = match self.raw[jet_step] {
                '>' => {
                    Direction::Right.value()
                }
                '<' => {
                    Direction::Left.value()
                }
                _ => panic!("Uh oh")
            };
            jet_step = (jet_step + 1) % self.raw.len();
            let mut block = block_opt.as_ref().unwrap().clone();
            block.shift(&shift);
            if self.is_collision(&block) {
                block.shift(&(Point {x: 0, y: 0} - shift));
            }
            block.shift(&(Direction::Down.value()));
            block_opt = Some(block.clone());
            if self.is_collision(&block) {
                block.shift(&(Direction::Up.value()));
                for point in block.map.iter() {
                    self.map.insert(point.clone());
                }
                top_y = top_y.max(block.top().y);
                block_opt = None;
                rocks += 1;
                end_rock_count += 1;
                if rocks_remaining.is_some() && end_rock_count == rocks_remaining.unwrap() {
                    let height_change = (top_y + 1) - offset_height;
                    return height_change + height_after_cycles;
                }
            }
        }
    }
    fn is_collision(&self, block: &Block) -> bool {
        if block.left().x <= WALL_LEFT {
            return true
        }
        if block.right().x >= WALL_RIGHT {
            return true
        }
        if block.bottom().y <= GROUND {
            return true
        }
        for point in block.map.iter() {
            if self.map.contains(point) {
                return true
            }
        }
        return false
    }
}

const WALL_LEFT: i64 = -1;
const WALL_RIGHT: i64 = 7;
const GROUND: i64 = -1;

fn part1() -> i64 {
    let data = get_data().trim().to_string();
    let data_chars = data.chars().map(|x| x).collect_vec();
    let mut chamber = Chamber::new(&data_chars);
    let y = chamber.run_simulation(2022);
    return y + 1
}

fn part2() -> i64 {
    let data = get_data().trim().to_string();
    let data_chars = data.chars().map(|x| x).collect_vec();
    let mut chamber = Chamber::new(&data_chars);
    let y = chamber.get_big_rocks(1_000_000_000_000);
    return y
}

fn get_data() -> String {
    return fs::read_to_string("../data/day17.txt").unwrap();
}

fn main() {
    let p1 = part1();
    println!("part 1: {}", p1);
    let p2 = part2();
    println!("part 2: {}", p2);
}
