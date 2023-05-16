use std::{fs, collections::HashMap};

#[derive(Debug, Clone)]
struct File {
    size: u64,
}

#[derive(Debug, Clone)]
struct Folder {
    name: String,
    size: Option<u64>,
}

#[derive(Debug)]
enum Node {
    File(File),
    Folder(Folder),
}

type Dir = HashMap<String, Vec<Node>>;

fn get_structure(data: String) -> Dir {
    let mut root: Dir = HashMap::new();
    let iter = data.trim().split("\n");
    let mut cwd = "".to_string();
    for line in iter {
        let mut parts = line.split_whitespace();
        let a = parts.next().unwrap();
        let b = parts.next().unwrap();
        let c = parts.next().unwrap_or("");
        match (a, b, c) {
            ("$", "cd", "/") => {
                cwd = "/".to_string();
                root.insert("/".to_string(), vec![]);
            }
            ("$", "ls", "") => {
                continue
            }
            ("$", "cd", _) => {
                if c == ".." {
                    let vec = cwd.split("/").collect::<Vec<&str>>();
                    let upto = vec.len() - 1;
                    let part = &vec[0..upto];
                    cwd = part.join("/");
                } else {
                    cwd = cwd.clone() + "/" + c;
                }
            }
            ("dir", _, "") => {
                let mut cwd_string = cwd.to_string();
                cwd_string = cwd_string + "/" + b;
                let folder = Node::Folder(Folder {
                    name: cwd_string.clone(),
                    size: None,
                });
                if let Some(vec) = root.get_mut(&cwd) {
                    vec.push(folder);
                } else {
                    root.insert(cwd.clone(), vec![folder]);
                }
            }
            (_, _, "") => {
                let size: u64 = a.parse().unwrap();
                let file = Node::File(File {
                    size,
                });
                if let Some(vec) = root.get_mut(&cwd) {
                    vec.push(file);
                } else {
                    root.insert(cwd.clone(), vec![file]);
                }
            }
            _ => {
                panic!("Should not have gotten here either")
            }
        }
    }
    return root;
}

fn get_size(root: &Dir, path: &String) -> u64 {
    let mut total = 0u64;
    if let Some(val) = root.get(&path.clone()) {
        for node in val {
            match node {
                Node::Folder(x) => {
                    if x.size == None {
                        total += get_size(&root, &x.name);
                    }
                }
                Node::File(x) => {
                    total += x.size;
                }
            }
        }
    }
    return total
}

fn part1() -> u64 {
    let data = fs::read_to_string("../data/day7.txt").unwrap();
    let root = get_structure(data);
    let mut total = 0u64;
    for path in root.keys() {
        let size = get_size(&root, path);
        if size <= 100000 {
            total += size;
        }
    }
    return total;
}

fn find_smallest_dir_with_space(root: &Dir, space: &u64) -> u64 {
    let mut smallest_size = 1000000000000u64;
    for path in root.keys() {
        let size = get_size(&root, path);
        if &size >= space && size < smallest_size {
            smallest_size = size;
        }
    }
    return smallest_size;
}

fn part2() -> u64 {
    let data = fs::read_to_string("../data/day7.txt").unwrap();
    let root = get_structure(data);
    let total_needed = 30000000u64;
    let total_available = 70000000u64;
    let root_space = get_size(&root, &"/".to_string()) as u64;
    let space_needed = root_space - (total_available - total_needed);
    return find_smallest_dir_with_space(&root, &space_needed)
}


fn main() {
    let p1 = part1();
    println!("Part 1: {}", p1);
    let p2 = part2();
    println!("Part 2: {}", p2);
}
