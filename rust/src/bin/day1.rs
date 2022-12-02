use::std::fs;

type N = u32;
type VecN = Vec<N>;

fn main() {
    let data = fs::read_to_string("../data/day1.txt").unwrap();
    let mut ndata: VecN = data
        .trim()
        .split("\n\n")
        .map(|x| -> N {
            let nums: VecN = x.split("\n").map(|x| x.parse().unwrap()).collect();
            nums.iter().sum()
        })
        .collect();
    ndata.sort();
    ndata.reverse();
    println!("{:?}", ndata[0]);
    println!("{:?}", &ndata[..3].iter().sum::<N>());
}
