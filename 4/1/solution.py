#!/usr/bin/env python
from dataclasses import dataclass
from typing import List, Set
import re

@dataclass
class Game:
    gid: int
    winners: Set[int]
    guesses: Set[int]

    def wins(self):
        return self.guesses.intersection(self.winners)

with open('input.txt', 'r') as f:
    games: List[Game] = []
    lines = f.readlines()
    for line in lines:
        line = re.sub(r"\s+", " ", line)
        pre, _, guess = line.strip().partition("|")
        card, _, wins = pre.strip().partition(":")
        _, _, gid = card.strip().partition(" ")
        games.append(Game(int(gid), set(int(w) for w in wins.strip().split(" ")), set(int(g) for g in guess.strip().split(" "))))

    if False:
        for g in games:
            print(f"{g.gid}: {g.wins()}")
    total = sum((pow(2, len(g.wins()) - 1) for g in games if len(g.wins()) > 0))
    print(f"Games: {len(games)}, sum: {total}")