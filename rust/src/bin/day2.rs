use std::collections::HashMap;
use std::fs;

fn main() {
    let choices: HashMap<&str, usize> = HashMap::from([
        ("A", 0),
        ("X", 0),
        ("B", 1),
        ("Y", 1),
        ("C", 2),
        ("Z", 2),
    ]);

    let data = fs::read_to_string("../data/day2.txt").unwrap();
    let parsed = data
        .trim()
        .split("\n")
        .map(|x| {
            x.split_whitespace()
                .map(|ch| choices.get(&ch).unwrap())
                .collect::<Vec<&usize>>()
        })
        .collect::<Vec<Vec<&usize>>>();
    let part1 = get_score(&parsed, false);
    let part2 = get_score(&parsed, true);
    println!("Part 1: {:?}", part1);
    println!("Part 2: {:?}", part2);
}

fn get_score(data: &Vec<Vec<&usize>>, alt: bool) -> usize {
    let mut score = 0;
    for item in data {
        let a = item[0];
        let b = if alt == true {
            let b = item[1];
            (a + (b + 2) % 3) % 3
        } else {
            *item[1]
        };
        let modu = (b + 3 - a) % 3;
        score += (3 * (1 + modu)) % 9 + b + 1;
    }
    score
}
