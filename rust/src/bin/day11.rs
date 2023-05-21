use num::integer::lcm;
use std::fs;

#[derive(Debug)]
enum Operation {
    Add(i64),
    Mult(i64),
    Square,
}

#[derive(Debug)]
struct Monkey {
    items: Vec<i64>,
    operation: Operation,
    test: i64,
    if_true: usize,
    if_false: usize,
    inspection_count: i64,
}

impl From<String> for Monkey {
    fn from(value: String) -> Self {
        let mut lines = value.lines();
        lines.next();
        let a = lines.next().unwrap();
        let b = lines.next().unwrap();
        let c = lines.next().unwrap();
        let d = lines.next().unwrap();
        let e = lines.next().unwrap();
        let items = a
            .split(":")
            .last()
            .unwrap()
            .trim()
            .split(",")
            .map(|x| x.trim().parse::<i64>().unwrap())
            .collect();
        let mut bparts = b.split("=").last().unwrap().trim().split_whitespace();
        bparts.next();
        let op = bparts.next().unwrap();
        let opvalue = bparts.next().unwrap().parse::<i64>();
        let operation = match (op, opvalue) {
            ("*", Err(_)) => Operation::Square,
            ("*", Ok(opvalue)) => Operation::Mult(opvalue),
            ("+", Ok(opvalue)) => Operation::Add(opvalue),
            _ => {
                panic!("what")
            }
        };
        let test = c.split_whitespace().last().unwrap().parse::<i64>().unwrap();
        let if_true = d
            .split_whitespace()
            .last()
            .unwrap()
            .parse::<usize>()
            .unwrap();
        let if_false = e
            .split_whitespace()
            .last()
            .unwrap()
            .parse::<usize>()
            .unwrap();
        Self {
            items,
            operation,
            test,
            if_true,
            if_false,
            inspection_count: 0,
        }
    }
}

impl Monkey {
    fn throw_to(&mut self, item_id: usize, maximum_worry: bool, divisor: i64) -> usize {
        self.inspection_count += 1;
        let item = self.items[item_id];
        let mut val = match self.operation {
            Operation::Add(x) => item + x,
            Operation::Mult(x) => item * x,
            Operation::Square => item.pow(2),
        };
        if !maximum_worry {
            val = val / 3;
        }
        if divisor != 0 {
            val = val % divisor;
        }
        self.items[item_id] = val;
        if val % self.test == 0 {
            return self.if_true;
        } else {
            return self.if_false;
        }
    }
}

fn get_lcm(monkeys: &Vec<Monkey>) -> i64 {
    let mut low = lcm(monkeys[0].test, monkeys[1].test);
    for monkey in monkeys[2..].iter() {
        low = lcm(low, monkey.test);
    }
    return low;
}

fn do_round(monkeys: &mut Vec<Monkey>, maximum_worry: bool, divisor: i64) {
    for i in 0..monkeys.len() {
        for j in 0..monkeys[i].items.len() {
            let monkey = &mut monkeys[i];
            let throw_to = monkey.throw_to(j, maximum_worry, divisor);
            let item_id = monkey.items[j].clone();
            monkeys[throw_to].items.push(item_id);
        }
        monkeys[i].items = vec![];
    }
}

fn part1() -> i64 {
    let data = get_data();
    let mut monkeys = get_monkeys(&data);
    let lcm_num = get_lcm(&monkeys);
    for _ in 0..20 {
        do_round(&mut monkeys, false, lcm_num);
    }
    monkeys.sort_by_key(|x| -x.inspection_count);
    let out = monkeys[0].inspection_count * monkeys[1].inspection_count;
    return out;
}

fn part2() -> i64 {
    let data = get_data();
    let mut monkeys = get_monkeys(&data);
    let lcm_num = get_lcm(&monkeys);
    for _ in 0..10_000 {
        do_round(&mut monkeys, true, lcm_num);
    }
    monkeys.sort_by_key(|x| -x.inspection_count);
    let out = monkeys[0].inspection_count * monkeys[1].inspection_count;
    return out;
}

fn get_data() -> String {
    let data = fs::read_to_string("../data/day11.txt").unwrap();
    return data;
}

fn get_monkeys(data: &String) -> Vec<Monkey> {
    let mut monkey_list = vec![];
    for paragraph in data.split("\n\n") {
        monkey_list.push(Monkey::from(paragraph.to_string()));
    }
    monkey_list
}

fn main() {
    let p1 = part1();
    println!("Part 1: {}", p1);
    let p2 = part2();
    println!("Part 2: {}", p2);
}
