#!/usr/bin/env python
from dataclasses import dataclass
from typing import List, Tuple
import re

# Maximums
# 12 red cubes, 13 green cubes, and 14 blue cubes
@dataclass
class Pixel:
    r: int
    g: int
    b: int

    @staticmethod
    def from_str(s: str) -> "Pixel":
        values = s.split(",")
        r = int(next((v.strip().split(" ")[0] for v in values if "red" in v), "0"))
        g = int(next((v.strip().split(" ")[0] for v in values if "green" in v), "0"))
        b = int(next((v.strip().split(" ")[0] for v in values if "blue" in v), "0"))
        return Pixel(r, g, b)

    def possible(self, other):
        return (self.r <= other.r and
                self.g <= other.g and
                self.b <= other.b)


LIMIT = Pixel(12, 13, 14)


@dataclass
class Game:
    gid: int
    pixels: List[Pixel]

    def possible(self):
        return all((p.possible(LIMIT) for p in self.pixels))


games: List[Game] = []
with open('input.txt', 'r') as f:
    lines = f.readlines()
    for line in lines:
        pre, _, post = line.partition(":")
        gid = int(pre.strip().split(" ")[1])
        pixels = [Pixel.from_str(s.strip()) for s in post.strip().split(";")]
        games.append(Game(gid, pixels))
    assert(len(games) == len(lines))

for g in games:
    if not g.possible():
        print(f"reject: {g}")

for g in games:
    if g.possible():
        print(f"accept: {g}")

total = sum((g.gid for g in games if g.possible()))
print(f"Count: {len(games)}, Sum: {total}")
