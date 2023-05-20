use std::{collections::HashMap, fs};

fn main() {
    let data = fs::read_to_string("../data/day6.txt").unwrap();
    let data = data.trim();

    let p1 = find_start(data, 4);
    let p2 = find_start(data, 14);

    println!("Part 1: {:?}", p1);
    println!("Part 2: {:?}", p2);
}

fn find_start(data: &str, count: usize) -> usize {
    let mut letters: HashMap<char, usize> = HashMap::new();
    let data_chars: Vec<char> = data.chars().collect();
    for i in 0..count {
        let ch = data_chars[i];
        if let Some(val) = letters.get_mut(&ch) {
            *val += 1;
        } else {
            letters.insert(ch.clone(), 1);
        }
    }
    for i in count..data_chars.len() {
        if letters.len() == count {
            return i
        }
        let ch = data_chars[i-count];
        if let Some(val) = letters.get_mut(&ch) {
            if val == &mut 1 {
                letters.remove(&ch);
            }
            else {
                *val -= 1;
            }
        }
        let ch = data_chars[i];
        if let Some(val) = letters.get_mut(&ch) {
            *val += 1;
        } else {
            letters.insert(ch.clone(), 1);
        }
    }
    panic!("Expected to find value before ending loop.");
}
