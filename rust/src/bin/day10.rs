use std::fs;

enum Instruction {
    Noop,
    Addx(i32),
}

fn main() {
    let data = get_data();
    let instructions = parse_instructions(&data);
    let values = get_values(&instructions);
    let p1 = part1(&values);
    println!("Part 1: {}", p1);
    let p2 = get_output(&values);
    println!("{}", p2);
}

fn part1(values: &Vec<i32>) -> i32 {
    return get_signal_strengths(values);
}

fn get_data() -> String {
    let data = fs::read_to_string("../data/day10.txt").unwrap();
    return data;
}

fn get_values(instructions: &Vec<Instruction>) -> Vec<i32> {
    let mut values = vec![1 as i32];
    for instr in instructions.into_iter() {
        values.push(values.last().unwrap().clone());
        if let Instruction::Addx(val) = instr {
            values.push(values.last().unwrap().clone() + val);
        }
    }
    return values;
}

fn get_signal_strengths(values: &Vec<i32>) -> i32 {
    let mut i = 20;
    let mut total = 0;
    while i < 221 {
        total += values[i - 1] * i as i32;
        i += 40;
    }
    return total;
}

fn get_output(values: &Vec<i32>) -> String {
    let mut output: Vec<String> = vec![];
    let mut row: Vec<&str> = vec![];
    for (i, val) in values.iter().enumerate() {
        let x = i % 40;
        let cycle = x + 1;
        if x == 0 && !row.is_empty() {
            output.push(row.join(""));
            row = vec![];
        }
        row.push(
            if [val.clone(), val + 1, val + 2].contains(&(cycle as i32)) {
                "#"
            } else {
                "."
            },
        );
    }
    return output.join("\n");
}

fn parse_instructions(data: &String) -> Vec<Instruction> {
    let mut instructions = Vec::new();
    for line in data.lines() {
        let mut parts = line.split_whitespace();
        let a = parts.next().unwrap();
        let b = parts.next().unwrap_or("").parse::<i32>();
        match (a, b) {
            ("noop", Err(_)) => {
                instructions.push(Instruction::Noop);
            }
            ("addx", Ok(b)) => {
                instructions.push(Instruction::Addx(b));
            }
            _ => {
                panic!("")
            }
        }
    }
    return instructions;
}
