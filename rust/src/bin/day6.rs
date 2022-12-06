use std::{collections::HashSet, fs};

fn main() {
    let data = fs::read_to_string("../data/day6.txt").unwrap();
    let data = data.trim();

    let p1 = find_start(data, 4);
    let p2 = find_start(data, 14);

    println!("Part 1: {:?}", p1);
    println!("Part 2: {:?}", p2);
}

fn find_start(data: &str, count: usize) -> usize {
    for i in 0..data.len() {
        let letters: HashSet<char> = data[i..i+count].chars().collect();
        if letters.len() == count {
            return i + count
        }
    }
    panic!("Expected to find value before ending loop.");
}
