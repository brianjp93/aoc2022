use core::panic;
use std::{rc::{Rc, Weak}, cell::{RefCell, Cell}, fs, println};


#[derive(Default, Debug)]
struct Tree {
    root: Rc<RefCell<Folder>>
}

#[derive(Debug, Default)]
struct File {
    name: String,
    size: u64,
}

#[derive(Debug, Default)]
struct FolderInner {
    name: String,
    size: Cell<u64>,
    files: RefCell<Vec<File>>,
    folders: RefCell<Vec<Folder>>,
    parent: Option<Weak<FolderInner>>
}

#[derive(Debug, Default)]
struct Folder(Rc<FolderInner>);

impl Folder {
    fn cd(&mut self, path: String) -> Rc<FolderInner> {
        if path == "..".to_string() {
            let folder = self.0.parent.as_ref().unwrap().upgrade().unwrap();
            return folder;
        }
        for folder in self.0.folders.borrow().iter() {
            if folder.0.name == path {
                return folder.0.clone();
            }
        }
        let mut folderinner = FolderInner::default();
        folderinner.name = path;
        folderinner.parent = Some(Rc::downgrade(&self.0));
        let folder = Folder {0: Rc::new(folderinner)};
        let rcinner = folder.0.clone();
        self.0.folders.borrow_mut().push(folder);
        return rcinner;
    }
    fn size(&self) -> u64 {
        if self.0.size.get() > 0 {
            return self.0.size.get();
        }
        let file_size: u64 = self.0.files.borrow().iter().map(|file| file.size).sum();
        let folder_size: u64 = self.0.folders.borrow().iter().map(|folder| folder.size()).sum();
        self.0.size.set(folder_size + file_size);
        return folder_size + file_size
    }
    fn get_all_folder_size(&self, size: u64) -> u64 {
        let mut total = 0;
        if self.size() <= size {
            total += self.size();
        }
        for folder in self.0.folders.borrow().iter() {
            total += folder.get_all_folder_size(size);
        }
        return total
    }
    fn add_file(&self, filename: String, size: u64) {
        for file in self.0.files.borrow().iter() {
            if file.name == filename {
                return
            }
        }
        self.0.files.borrow_mut().push(File {name: filename, size})
    }
}

fn get_structure(data: &String) -> Tree {
    let root = Tree::default();
    let mut cwd = root.root.clone();
    for line in data.trim().split("\n") {
        let mut parts = line.split_whitespace();
        let a = parts.next().unwrap();
        let b = parts.next().unwrap();
        let c = parts.next().unwrap_or("");
        match (a, b, c) {
            ("$", "cd", "/") | ("$", "ls", "") | ("dir", _, "") => {
                // these don't actually matter
                continue
            }
            ("$", "cd", _) => {
                let new_cwd = Rc::new(RefCell::new(Folder {0: cwd.borrow_mut().cd(c.to_string())}));
                cwd = new_cwd;
            }
            (_, _, "") => {
                let size: u64 = a.parse().unwrap();
                cwd.borrow().add_file(b.to_string(), size);
            }
            _ => {
                panic!("how did you get here")
            }
        }
    }
    return root;
}

fn find_smallest_dir_with_space(root: &Tree, space_needed: u64) -> u64 {
    let x = root.root.borrow().0.clone();
    let mut check = vec![x];
    let mut smallest = 100000000000000u64;
    while let Some(finner) = check.pop() {
        let size = finner.size.get();
        if size >= space_needed && size < smallest {
            smallest = size;
        }
        check.append(&mut finner.folders.borrow().iter().map(|x| x.0.clone()).collect::<Vec<_>>());
    }
    return smallest;
}

fn part1() -> u64 {
    let data = fs::read_to_string("../data/day7.txt").unwrap();
    let root = get_structure(&data);
    let size = root.root.borrow().get_all_folder_size(100000);
    return size
}

fn part2() -> u64 {
    let data = fs::read_to_string("../data/day7.txt").unwrap();
    let root = get_structure(&data);
    let total_needed = 30000000u64;
    let total_available = 70000000u64;
    let root_space = root.root.borrow().size();
    let space_needed = root_space - (total_available - total_needed);
    let size = find_smallest_dir_with_space(&root, space_needed);
    return size
}

fn main() {
    let p1 = part1();
    println!("part 1: {}", p1);
    let p2 = part2();
    println!("part 2: {}", p2);
}
