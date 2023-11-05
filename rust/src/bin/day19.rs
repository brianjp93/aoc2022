use std::fs;
use regex::Regex;


#[derive(Debug)]
struct Resources {
    ore: i64,
    clay: i64,
    obsidian: i64,
    geode: i64,
}

#[derive(Debug)]
struct BluePrint {
    ore: Resources,
    clay: Resources,
    obsidian: Resources,
    geode: Resources,
}

struct Robots {
    ore: i64,
    clay: i64,
    obsidian: i64,
    geode: i64,
}


fn part1() -> i64 {
    let data = get_data().trim().to_string();
    let reg = Regex::new(r"Blueprint \d+:.*?(\d+).*?(\d+).*?(\d+).*?(\d+).*?(\d+).*?(\d+)").unwrap();
    let mut blueprints: Vec<BluePrint> = vec![];
    for cap in reg.captures_iter(&data) {
        let a: i64 = cap.get(1).unwrap().as_str().parse().unwrap();
        let b: i64 = cap.get(2).unwrap().as_str().parse().unwrap();
        let c: i64 = cap.get(3).unwrap().as_str().parse().unwrap();
        let d: i64 = cap.get(4).unwrap().as_str().parse().unwrap();
        let e: i64 = cap.get(5).unwrap().as_str().parse().unwrap();
        let f: i64 = cap.get(6).unwrap().as_str().parse().unwrap();
        let bp = BluePrint {
            ore: Resources {
                ore: a,
                clay: 0,
                obsidian: 0,
                geode: 0,
            },
            clay: Resources {
                ore: b,
                clay: 0,
                obsidian: 0,
                geode: 0,
            },
            obsidian: Resources {
                ore: c,
                clay: d,
                obsidian: 0,
                geode: 0,
            },
            geode: Resources {
                ore: e,
                clay: 0,
                obsidian: f,
                geode: 0,
            },
        };
        blueprints.push(bp);
    }
    println!("{:?}", blueprints);
    0
}

// fn part2() -> i64 {
//     let data = get_data().trim().to_string();
// }

fn get_data() -> String {
    return fs::read_to_string("../data/day19.txt").unwrap();
}

fn main() {
    let p1 = part1();
    // println!("part 1: {}", p1);
    // let p2 = part2();
    // println!("part 2: {}", p2);
}
