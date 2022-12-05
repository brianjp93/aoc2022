use regex::Regex;
use std::{fs, cmp};

fn main() {
    let data = fs::read_to_string("../data/day5.txt").unwrap();
    let (mut crates, instructions) = parse(&data);

    for (count, from, to) in instructions {
        let len = crates[from].len();
        let move_count = cmp::max(0, len-count);
        let mut piece = crates[from].drain(move_count..).collect::<Vec<_>>();
        piece.reverse();
        crates[to].extend(piece);
    }
    let p1: Vec<_> = crates.iter().map(|x| x.last().unwrap()).collect();

    let (mut crates, instructions) = parse(&data);
    for (count, from, to) in instructions {
        let len = crates[from].len();
        let move_count = cmp::max(0, len-count);
        let piece = crates[from].drain(move_count..).collect::<Vec<_>>();
        crates[to].extend(piece);
    }
    let p2: Vec<_> = crates.iter().map(|x| x.last().unwrap()).collect();

    println!("Part 1: {:?}", p1);
    println!("Part 2: {:?}", p2);
}

fn parse(data: &String) -> (Vec<Vec<char>>, Vec<(usize, usize, usize)>) {
    let mut crates: Vec<Vec<char>> = Vec::new();
    let parts = data.split("\n\n").collect::<Vec<_>>();
    let a = parts[0];
    let b = parts[1];

    let lines = a.split("\n").collect::<Vec<_>>();
    let mut i = 0;
    let max_len = lines.last().unwrap().len();
    let mut idx = i * 4 + 1;
    while idx < max_len {
        let mut row = lines[0..lines.len()-1].iter().map(|line| {
            line.chars().collect::<Vec<_>>()[idx]
        }).filter(|x| x != &' ').collect::<Vec<char>>();
        i += 1;
        idx = i * 4 + 1;
        row.reverse();
        crates.push(row);
    }

    let re = Regex::new(r"move (\d+) from (\d+) to (\d+)").unwrap();
    let mut instructions: Vec<(usize, usize, usize)> = Vec::new();
    for item in re.captures_iter(b) {
        let count = item.get(1).unwrap().as_str().parse::<usize>().unwrap();
        let from = item.get(2).unwrap().as_str().parse::<usize>().unwrap() - 1;
        let to = item.get(3).unwrap().as_str().parse::<usize>().unwrap() - 1;
        instructions.push((count, from , to));
    }
    (crates, instructions)
}
