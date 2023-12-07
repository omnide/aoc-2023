#!/usr/bin/env python
from dataclasses import dataclass
from typing import List, Optional, Set
import re

@dataclass
class Game:
    gid: int
    winners: Set[int]
    guesses: Set[int]
    copies: int = 1

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

    # Conduction expansion pass to get additional plays
    for i, g in enumerate(games):
        w = len(g.wins())
        if w == 0:
            continue

        for j in range(0, w):
            if i+1+j >= len(games):
                break
            games[i+1+j].copies += games[i].copies
    
    total_cards = sum((g.copies for g in games))
    print(f"Games: {len(games)}, sum: {total_cards}")