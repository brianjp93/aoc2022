use std::{collections::HashSet, fs, cmp};
use regex::Regex;

fn main() {
    let data = fs::read_to_string("../data/day4.txt").unwrap();

    let mut count1 = 0;
    let mut count2 = 0;

    let re = Regex::new(r"(\d+)-(\d+),(\d+)-(\d+)").unwrap();
    for cap in re.captures_iter(&data) {
        let a: usize = cap.get(1).unwrap().as_str().parse().unwrap();
        let b: usize = cap.get(2).unwrap().as_str().parse().unwrap();
        let c: usize = cap.get(3).unwrap().as_str().parse().unwrap();
        let d: usize = cap.get(4).unwrap().as_str().parse().unwrap();
        let r1: HashSet<usize> = HashSet::from_iter(a..b+1);
        let r2: HashSet<usize> = HashSet::from_iter(c..d+1);

        if r1.union(&r2).count() == cmp::max(r1.len(), r2.len()) {
            count1 += 1;
        }
        if r1.intersection(&r2).count() > 0 {
            count2 += 1;
        }
    }
    println!("Part 1: {}", count1);
    println!("Part 2: {}", count2);
}
