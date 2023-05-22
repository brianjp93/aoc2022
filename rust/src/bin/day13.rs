use std::cmp::Ordering;
use std::fs;

#[derive(Debug, Clone)]
enum Node {
    Item(i32),
    List(Vec<Node>),
}

fn build_node(data: &str) -> (Node, usize) {
    let mut items: Vec<Node> = Vec::new();
    let mut digit_list: Vec<String> = vec![];
    let mut i = 1;
    let datachars = data.chars().collect::<Vec<_>>();
    let mut ch: char;
    while i < data.len() {
        ch = datachars[i];
        match ch {
            '[' => {
                let (item, idx) = build_node(&data[i..]);
                i = idx + i;
                items.push(item);
            }
            ']' => {
                if !digit_list.is_empty() {
                    let num = digit_list.join("").parse::<i32>().unwrap();
                    items.push(Node::Item(num));
                    digit_list.clear();
                }
                return (Node::List(items), i + 1);
            }
            ',' => {
                if !digit_list.is_empty() {
                    let num = digit_list.join("").parse::<i32>().unwrap();
                    items.push(Node::Item(num));
                    digit_list.clear();
                }
            }
            _ => {
                if ch.is_ascii_digit() {
                    digit_list.push(ch.to_string());
                }
            }
        }
        i += 1;
    }
    return (Node::List(items), 0);
}

fn parse_data(data: &str) -> Vec<(Node, Node)> {
    let mut groups: Vec<(Node, Node)> = vec![];
    for group in data.split("\n\n") {
        let mut parts = group.lines();
        let a = parts.next().unwrap();
        let b = parts.next().unwrap();
        let (node1, _) = build_node(a);
        let (node2, _) = build_node(b);
        groups.push((node1, node2));
    }
    return groups;
}

fn compare(a: &Node, b: &Node) -> Ordering {
    match (a, b) {
        (Node::List(x), Node::List(y)) => {
            for (c, d) in x.iter().zip(y.iter()) {
                let result = compare(c, d);
                if result != Ordering::Equal {
                    return result;
                }
            }
            if x.len() < y.len() {
                return Ordering::Less;
            } else if x.len() > y.len() {
                return Ordering::Greater;
            }
            return Ordering::Equal;
        }
        (Node::Item(x), Node::Item(y)) => {
            if x < y {
                return Ordering::Less;
            } else if x == y {
                return Ordering::Equal;
            }
            return Ordering::Greater;
        }
        (Node::List(_), Node::Item(_)) => return compare(a, &Node::List(vec![b.clone()])),
        (Node::Item(_), Node::List(_)) => return compare(&Node::List(vec![a.clone()]), b),
    }
}

fn part1() -> i32 {
    let data = get_data();
    let groups = parse_data(&data);
    let out: i32 = groups
        .iter()
        .enumerate()
        .filter_map(|(i, x)| {
            if compare(&x.0, &x.1) == Ordering::Less {
                return Some((i + 1) as i32);
            };
            None
        })
        .sum();
    return out;
}

fn part2() -> i32 {
    let mut nodes: Vec<&Node> = vec![];
    let mut data = get_data().trim().to_string();
    data = data + "\n\n[[2]]\n[[6]]";
    let decoder1 = Node::List(vec![Node::List(vec![Node::Item(2)])]);
    let decoder2 = Node::List(vec![Node::List(vec![Node::Item(6)])]);
    let groups = parse_data(&data);
    for x in groups.iter() {
        nodes.push(&x.0);
        nodes.push(&x.1);
    }
    nodes.sort_by(|a, b| return compare(a, b));
    let mut prod = 1 as i32;
    for (i, node) in nodes.iter().enumerate() {
        if compare(node, &decoder1) == Ordering::Equal
            || compare(node, &decoder2) == Ordering::Equal
        {
            prod = prod * (i + 1) as i32;
        }
    }
    return prod;
}

fn get_data() -> String {
    let data = fs::read_to_string("../data/day13.txt").unwrap();
    return data;
}

fn main() {
    let p1 = part1();
    println!("Part 1: {}", p1);
    let p2 = part2();
    println!("Part 2: {}", p2);
}
