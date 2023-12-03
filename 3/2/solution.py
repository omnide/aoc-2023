#!/usr/bin/env python
from dataclasses import dataclass
from itertools import chain
from typing import List, Optional, Tuple
import re

GREEN = "\033[32m"
RED = "\033[31m"

@dataclass
class Cell:
    content: str
    x: int
    y: int

    color: str = ""

    def is_symbol(self) -> bool:
        return self.content != "." and not self.content.isdigit()

    def maybe_gear(self) -> bool:
        return self.content == "*"


@dataclass
class Grid:
    """ Make a grid to ease lookups, and print for debugging """

    grid: List[List[Cell]]
    row_count: int
    col_count: int

    def __init__(self, grid: List[str]):
        g: List[List[Cell]] = []
        for i, row in enumerate(grid):
            row_cells: List[Cell] = []
            for j, char in enumerate(row.rstrip()):
                row_cells.append(Cell(char, j, i))
            g.append(row_cells)
        self.grid = g
        self.row_count = len(self.grid)
        self.col_count = len(self.grid[0])
    
    def cell(self, x: int, y: int) -> Optional[Cell]:
        if x < 0 or y < 0 or x >= self.col_count or y >= self.row_count:
            return None
        return self.grid[y][x % self.col_count]

    def print_grid(self):
        for row in self.grid:
            txt = ""
            for cell in row:
                if cell.color:
                    txt += cell.color + cell.content + "\033[0m"
                else:
                    txt += cell.content
            print(txt)



@dataclass
class Number:
    content: str
    x1: int
    x2: int
    y: int

    def adjacent_cells(self, grid: Grid) -> List[Cell]:
        corners = [
            (self.x1 - 1, self.y - 1), # top left
            (self.x2 + 1, self.y - 1), # top right
            (self.x1 - 1, self.y + 1), # bottom left
            (self.x2 + 1, self.y + 1), # bottom right
        ]
        above = [(x, self.y - 1) for x in range(self.x1, self.x2 + 1)]
        below = [(x, self.y + 1) for x in range(self.x1, self.x2 + 1)]
        lr = [(self.x1 - 1, self.y), (self.x2 + 1, self.y)]
        adjacent: List[Cell] = []
        for x, y in corners + above + below + lr:
            cell = grid.cell(x, y)
            if cell:
                adjacent.append(cell)
        return adjacent
        
    def is_part(self, grid: Grid) -> bool:
        return any((c.is_symbol() for c in self.adjacent_cells(grid)))

    def contains_cell(self, cell: Cell) -> bool:
        return self.x1 <= cell.x <= self.x2 and self.y == cell.y

    def color_cells(self, grid: Grid, color: str):
        for x in range(self.x1, self.x2 + 1):
            grid.cell(x, self.y).color = color


with open('input.txt', 'r') as f:
    lines = f.readlines()
    grid: Grid = Grid(lines)
    numbers: List[List[Number]] = [list() for _ in range(grid.row_count)]

    # Just use the original line text and regex to speed number identification
    for i, row in enumerate(lines):
        for m in re.finditer(r"(\d+)", row):
            num = m.group(1)
            numbers[i].append(Number(num, m.start(), m.end() - 1, i))
    
    # Some quick sanity checks
    for n in chain(*numbers):
        for i, c in enumerate(n.content):
            assert c.isdigit()
            assert grid.cell(n.x1 + i, n.y).content == c
        assert n.x2 - n.x1 + 1 == len(n.content), f"Bad number string len: {n.content} {n.x1} {n.x2}"

    # Find the gears
    gears: List[Tuple[Cell, Number, Number]] = []
    for y, row in enumerate(grid.grid):
        for x, cell in enumerate(row):
            if not cell.maybe_gear():
                continue
            adjacent_numbers: List[Number] = []
            for r in (y - 1, y, y + 1):
                if r < 0 or r >= grid.row_count:
                    continue
                for n in numbers[r]:
                    if cell in n.adjacent_cells(grid):
                        adjacent_numbers.append(n)

            # Gears have exactly two adjacent numbers
            if len(adjacent_numbers) == 2:
                gears.append((cell, adjacent_numbers[0], adjacent_numbers[1]))
                
    total = sum((int(n1.content) * int(n2.content) for _, n1, n2 in gears))
    if False:
        for c, n1, n2 in gears:
            c.color = GREEN
            n1.color_cells(grid, RED)
            n2.color_cells(grid, RED)
        grid.print_grid()
    print(f"Count: {len(gears)} gears, Sum: {total}")