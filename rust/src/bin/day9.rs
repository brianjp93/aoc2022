use std::{
    collections::HashSet,
    fs,
    hash::{Hash, Hasher},
    ops::{Add, Sub},
};

#[derive(Debug, Copy, Clone, PartialEq, Default, Eq)]
struct Point {
    x: i32,
    y: i32,
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

struct Instruction {
    direction: Direction,
    count: i32,
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

impl Instruction {
    fn get_instructions(data: &str) -> Vec<Self> {
        let mut instructions: Vec<Self> = vec![];
        for line in data.trim().lines() {
            let mut parts = line.split_whitespace();
            let direction = match parts.next().unwrap() {
                "U" => Direction::Up,
                "D" => Direction::Down,
                "R" => Direction::Right,
                "L" => Direction::Left,
                _ => {
                    panic!("Unknown command.");
                }
            };
            let count = parts.next().unwrap().parse::<i32>().unwrap();
            instructions.push(Instruction { direction, count });
        }
        return instructions;
    }
}

struct Rope {
    rope: Vec<Point>,
    l_history: HashSet<Point>,
}

impl Rope {
    fn new(rope_length: i32) -> Self {
        let mut rope: Vec<Point> = vec![];
        for _ in 0..rope_length {
            rope.push(Point::default());
        }
        return Self {
            rope,
            l_history: HashSet::new(),
        };
    }
    fn do_moves(&mut self, instructions: &Vec<Instruction>) {
        for instr in instructions.iter() {
            self.do_move(instr);
        }
    }
    fn do_move(&mut self, instr: &Instruction) {
        for _ in 0..instr.count {
            self.rope[0] = self.rope[0] + instr.direction.value();
            for i in 0..self.rope.len() - 1 {
                let p1 = self.rope[i];
                let mut p2 = self.rope[i + 1];
                self.follow(p1, &mut p2);
                self.rope[i + 1] = p2;
            }
            self.l_history.insert(self.rope.last().unwrap().clone());
        }
    }
    fn follow(&self, p1: Point, p2: &mut Point) {
        let diff = p1 - *p2;
        let dx_unit = if diff.x != 0 {
            diff.x.abs() / diff.x
        } else {
            0
        };
        let dy_unit = if diff.y != 0 {
            diff.y.abs() / diff.y
        } else {
            0
        };
        if diff.x.abs() == 2 {
            (*p2).x += dx_unit;
            if diff.y.abs() >= 1 {
                (*p2).y += dy_unit;
            }
        } else if diff.y.abs() == 2 {
            (*p2).y += dy_unit;
            if diff.x.abs() >= 1 {
                (*p2).x += dx_unit;
            }
        }
    }
}

fn part1() -> usize {
    let data_string = get_data();
    let instructions = Instruction::get_instructions(&data_string);
    let mut rope = Rope::new(2);
    rope.do_moves(&instructions);
    let len = rope.l_history.len();
    return len;
}

fn part2() -> usize {
    let data_string = get_data();
    let instructions = Instruction::get_instructions(&data_string);
    let mut rope = Rope::new(10);
    rope.do_moves(&instructions);
    let len = rope.l_history.len();
    return len;
}

fn get_data() -> String {
    let data = fs::read_to_string("../data/day9.txt").unwrap();
    return data;
}

fn main() {
    let p1 = part1();
    println!("Part 1: {}", p1);
    let p2 = part2();
    println!("Part 2: {}", p2);
}
