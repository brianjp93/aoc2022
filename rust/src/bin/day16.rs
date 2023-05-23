use itertools::Itertools;
use std::{
    collections::{HashMap, HashSet},
    fs,
};

fn get_init_data() -> (ValveMap, HashSet<String>, String) {
    let data = get_data();
    let valves = parse(&data);
    let mut need_to_open: HashSet<String> = HashSet::new();
    for (key, val) in valves.iter() {
        if val.0 > 0 {
            need_to_open.insert(key.clone());
        }
    }
    let start = "AA".to_string();
    return (valves, need_to_open, start);
}

fn traverse(start: String, need_to_open: HashSet<String>, valves: ValveMap) -> i32 {
    let mut stack: Vec<(String, Option<String>, HashMap<String, i32>, i32)> =
        vec![(start, None, HashMap::new(), 30i32)];
    let mut maximum = 0;
    while let Some((valve, prev, opened, minutes)) = stack.pop() {
        let opened_keys = opened.keys().map(|x| x.clone()).collect::<HashSet<_>>();
        let valves_left: HashSet<String> = need_to_open
            .difference(&opened_keys)
            .map(|x| x.clone())
            .collect();
        let mut valves_left_values: Vec<i32> = valves_left
            .iter()
            .map(|x| valves.get(x).unwrap().0)
            .collect();
        valves_left_values.sort_by_key(|x| -x);
        let max_possible: i32 = valves_left_values
            .iter()
            .enumerate()
            .map(|(i, x)| return x * (minutes - ((i as i32) * 2i32)).max(0i32))
            .sum::<i32>()
            + opened.values().sum::<i32>();

        if max_possible <= maximum {
            continue;
        }
        if minutes <= 1 || valves_left.len() == 0 {
            maximum = maximum.max(opened.values().sum());
            continue;
        }
        let (rate, to_valves) = valves.get(&valve).unwrap();
        let next_minutes = minutes - 1;
        if !opened.contains_key(&valve) && rate > &0 {
            let mut next_opened = opened.clone();
            next_opened.insert(valve.clone(), next_minutes * rate);
            stack.push((
                valve.clone(),
                Some(valve.clone()),
                next_opened,
                next_minutes,
            ));
        }
        for next_valve in to_valves.iter() {
            if prev.clone().is_none() || prev.clone().unwrap() != *next_valve {
                stack.push((
                    next_valve.clone(),
                    Some(valve.clone()),
                    opened.clone(),
                    next_minutes,
                ));
            }
        }
    }
    return maximum;
}

fn double_traverse(start: String, need_to_open: HashSet<String>, valves: ValveMap) -> i32 {
    let mut stack: Vec<(
        String,
        String,
        Option<String>,
        Option<String>,
        HashMap<String, i32>,
        i32,
    )> = vec![(
        start.clone(),
        start.clone(),
        None,
        None,
        HashMap::new(),
        26i32,
    )];
    let mut maximum = 0;
    while let Some((valve1, valve2, prev1, prev2, opened, minutes)) = stack.pop() {
        let opened_keys = opened.keys().map(|x| x.clone()).collect::<HashSet<_>>();
        let valves_left: HashSet<String> = need_to_open
            .difference(&opened_keys)
            .map(|x| x.clone())
            .collect();
        let mut valves_left_values: Vec<i32> = valves_left
            .iter()
            .map(|x| valves.get(x).unwrap().0)
            .collect();
        valves_left_values.sort_by_key(|x| -x);
        let max_possible: i32 = valves_left_values
            .iter()
            .enumerate()
            .map(|(i, x)| return x * (minutes - (((i as i32) / 2) * 2i32)).max(0i32))
            .sum::<i32>()
            + opened.values().sum::<i32>();

        if max_possible <= maximum {
            continue;
        }
        if minutes <= 1 || valves_left.len() == 0 {
            maximum = maximum.max(opened.values().sum());
            continue;
        }
        let (rate1, mut to_valves1) = valves.get(&valve1).unwrap().clone();
        let (rate2, mut to_valves2) = valves.get(&valve2).unwrap().clone();
        if prev1.is_some() {
            let prev1_val = prev1.as_ref().unwrap().clone();
            to_valves1.remove(&prev1_val);
            to_valves2.remove(&prev1_val);
        }
        if prev2.is_some() {
            let prev2_val = prev2.as_ref().unwrap().clone();
            to_valves2.remove(&prev2_val);
            to_valves1.remove(&prev2_val);
        }
        to_valves1.remove(&valve2);
        to_valves2.remove(&valve1);
        let next_minutes = minutes - 1;
        if !opened.contains_key(&valve1) && rate1 > 0 {
            for next_valve2 in to_valves2.iter() {
                let mut next_opened = opened.clone();
                next_opened.insert(valve1.clone(), next_minutes * rate1);
                stack.push((
                    valve1.clone(),
                    next_valve2.clone(),
                    Some(valve1.clone()),
                    Some(valve2.clone()),
                    next_opened,
                    next_minutes,
                ));
            }
        }
        if !opened.contains_key(&valve2) && rate2 > 0 {
            for next_valve1 in to_valves1.iter() {
                let mut next_opened = opened.clone();
                next_opened.insert(valve2.clone(), next_minutes * rate2);
                stack.push((
                    next_valve1.clone(),
                    valve2.clone(),
                    Some(valve1.clone()),
                    Some(valve2.clone()),
                    next_opened,
                    next_minutes,
                ));
            }
        }
        if rate1 != 0
            && rate2 != 0
            && valve1 != valve2
            && !opened.contains_key(&valve1)
            && !opened.contains_key(&valve2)
        {
            let mut next_opened = opened.clone();
            next_opened.insert(valve1.clone(), next_minutes * rate1);
            next_opened.insert(valve2.clone(), next_minutes * rate2);
            stack.push((
                valve1.clone(),
                valve2.clone(),
                Some(valve1.clone()),
                Some(valve2.clone()),
                next_opened,
                next_minutes,
            ));
        }
        for (next_valve1, next_valve2) in to_valves1.iter().cartesian_product(to_valves2.iter()) {
            stack.push((
                next_valve1.clone(),
                next_valve2.clone(),
                Some(valve1.clone()),
                Some(valve2.clone()),
                opened.clone(),
                next_minutes,
            ));
        }
    }
    return maximum;
}

fn part1() -> i32 {
    let (valves, need_to_open, start) = get_init_data();
    let out = traverse(start, need_to_open, valves);
    return out;
}

fn part2() -> i32 {
    let (valves, need_to_open, start) = get_init_data();
    let out = double_traverse(start, need_to_open, valves);
    return out;
}

fn get_data() -> String {
    return fs::read_to_string("../data/day16.txt").unwrap();
}

type ValveMap = HashMap<String, (i32, HashSet<String>)>;

fn parse(data: &String) -> ValveMap {
    let mut valves: ValveMap = HashMap::new();
    let re = regex::Regex::new(r"Valve (\w+).*?(\d+).*?valve[s]? (.+)").unwrap();
    for m in re.captures_iter(&data) {
        let name = m.get(1).unwrap().as_str().to_string();
        let rate = m.get(2).unwrap().as_str().parse::<i32>().unwrap();
        let mut to_valve_set: HashSet<String> = HashSet::new();
        for item in m.get(3).unwrap().as_str().split(",") {
            to_valve_set.insert(item.trim().to_string());
        }
        valves.insert(name, (rate, to_valve_set));
    }
    return valves;
}

fn main() {
    let p1 = part1();
    println!("part 1: {}", p1);
    let p2 = part2();
    println!("part 2: {}", p2);
}
