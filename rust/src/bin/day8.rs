use std::{fs, println};

type ForestMap = Vec<Vec<i16>>;
#[derive(Debug)]
struct Forest {
    map: ForestMap,
}

impl Forest {
    fn count_visible(&self) -> i16 {
        let mut count = 0i16;
        for y in 0..self.map.len() {
            for x in 0..self.map[y].len() {
                if self.is_visible(x, y) {
                    count += 1;
                }
            }
        }
        count
    }
    fn inner_is_visible(&self, x: usize, y: usize) -> bool {
        let og_val = self.map[y][x];
        let mut xlow = (x - 1) as isize;
        while xlow >= 0 {
            let val = self.map[y][xlow as usize];
            if val >= og_val {
                break
            }
            xlow -= 1;
        }
        if xlow == -1 {
            return true
        }

        let mut xhigh = x + 1;
        while xhigh <= self.map[0].len() - 1 {
            let val = self.map[y][xhigh];
            if val >= og_val {
                break
            }
            xhigh += 1;
        }
        if xhigh == self.map[0].len() {
            return true
        }

        let mut ylow = (y - 1) as isize;
        while ylow >= 0 {
            let val = self.map[ylow as usize][x];
            if val >= og_val {
                break
            }
            ylow -= 1;
        }
        if ylow == -1 {
            return true
        }

        let mut yhigh = y + 1;
        while yhigh <= self.map.len() - 1 {
            let val = self.map[yhigh][x];
            if val >= og_val {
                break
            }
            yhigh += 1;
        }
        if yhigh == self.map.len() {
            return true
        }

        return false
    }
    fn is_visible(&self, x: usize, y: usize) -> bool {
        let max_x = self.map[0].len() - 1;
        let max_y = self.map.len() - 1;
        match (x, y) {
            (0, _) => {
                return true
            }
            (_, 0) => {
                return true
            }
            (x, y) => {
                if x == max_x || y == max_y {
                    return true
                }
                else {
                    return self.inner_is_visible(x, y)
                }
            }
        }
    }
    fn visibility_score(&self, x: isize, y: isize) -> i32 {
        let og = self.map[y as usize][x as usize];
        let mut distances: Vec<i32> = vec![];
        let width = self.map[0].len() as isize;
        let height = self.map.len() as isize;
        for dirs in [(1, 0), (-1, 0), (0, -1), (0, 1)] {
            let mut dx = x.clone();
            let mut dy = y.clone();
            let og_dx = dx.clone();
            let og_dy = dy.clone();
            let mut dist = 0;
            while dx >= 0 && dx < width && dy >= 0 && dy < height {
                if (x, y) != (dx, dy) && self.map[dy as usize][dx as usize] >= og {
                    break;
                }
                dx = (dirs.0 + (dx as i32)) as isize;
                dy = (dirs.1 + (dy as i32)) as isize;
                if dx < 0 || dx >= width || dy < 0 || dy >= height {
                    if (og_dx, og_dy) == (x, y) {
                        break
                    }
                }
                dist += 1;
            }
            distances.push(dist);
        }
        return distances.iter().product();
    }
    fn find_max_scenic_score(&self) -> i32 {
        let mut max_score = 0;
        for (y, row) in self.map.iter().enumerate() {
            for (x, _) in row.iter().enumerate() {
                let visibility = self.visibility_score(x as isize, y as isize);
                if visibility > max_score {
                    max_score = visibility;
                }
            }
        }
        return max_score;
    }
}

fn part1(data: &String) -> i16 {
    let data = parse_lines(&data);
    let forest = Forest { map: data.clone() };
    let visible = forest.count_visible();
    return visible
}

fn part2(data: &String) -> i32 {
    let data = parse_lines(&data);
    let forest = Forest { map: data.clone() };
    let score = forest.find_max_scenic_score();
    return score
}

fn get_data() -> String {
    let data = fs::read_to_string("../data/day8.txt").unwrap();
    return data;
}

fn parse_lines(data: &String) -> ForestMap {
    return data.lines().map(|line| {
        return line.chars().map(|ch| {
            return ch.to_string().parse().unwrap();
        }).collect();
    }).collect()
}

fn main() {
    let data = get_data();
    let p1 = part1(&data);
    println!("Part 1: {}", p1);
    let p2 = part2(&data);
    println!("Part 2: {}", p2);
}
