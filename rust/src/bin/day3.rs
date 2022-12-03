use std::{collections::HashSet, fs};

const LETTERS: &str = " abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";

fn main() {
    let data = fs::read_to_string("../data/day3.txt").unwrap();
    let p1: usize = data
        .trim()
        .split("\n")
        .map(|line| {
            let idx = line.len() / 2;
            let (a, b) = line.split_at(idx);
            get_score(vec![a, b])
        })
        .sum();
    println!("{:?}", p1);

    let p2: usize = data
        .trim()
        .split("\n")
        .collect::<Vec<&str>>()
        .chunks(3)
        .map(|item| get_score(item.to_vec()))
        .sum();
    println!("{:?}", p2);
}

fn get_score(args: Vec<&str>) -> usize {
    let sets = args
        .iter()
        .map(|arg| arg.chars().collect::<HashSet<char>>());
    let out = sets
        .reduce(|x, y| x.into_iter().filter(|item| y.contains(item)).collect())
        .unwrap();
    let letter = out.iter().next().unwrap();
    LETTERS.find(*letter).unwrap()
}
