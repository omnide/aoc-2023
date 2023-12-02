use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;

pub fn main() {
    let mut lc: i32 = 0;
    let mut total: i32 = 0;
    if let Ok(lines) = read_lines("input.txt") {
        for line in lines {
            if let Ok(content) = line {
                println!("{}", content);
                lc += 1;

                let mut first: i32 = -1;
                let mut last: i32 = -1;
                for c in content.chars() {
                    match c {
                        '0'..='9' => {
                            let num: i32 = c.to_digit(10).unwrap() as i32;
                            if first == -1 {
                                first = num;
                                last = num;
                            } else {
                                last = num;
                            }
                        }
                        _ => {}
                    }
                }
                total += (first * 10) + last;
            }
        }
    }
    println!("Count: {}, Sum: {}", lc, total);
}

fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where
    P: AsRef<Path>,
{
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}
