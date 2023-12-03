#!/usr/bin/env python
from dataclasses import dataclass
from typing import List, Optional, Tuple
import re

@dataclass
class Cell:
    content: str
    x: int
    y: int

    def is_symbol(self) -> bool:
        return self.content != "." and not self.content.isdigit()


@dataclass
class Grid:
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

    def print_grid(self, highlight_numbers: List["Number"] = []):
        for row in self.grid:
            txt = ""
            for cell in row:
                if any((n.contains_cell(cell) for n in highlight_numbers)):
                    txt += "\033[92m" + cell.content + "\033[0m"
                elif cell.is_symbol():
                    txt += "\033[91m" + cell.content + "\033[0m"
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


with open('input.txt', 'r') as f:
    numbers: List[Number] = []
    lines = f.readlines()
    grid: Grid = Grid(lines)
    for i, row in enumerate(lines):
        for m in re.finditer(r"(\d+)", row):
            num = m.group(1)
            numbers.append(Number(num, m.start(), m.end() - 1, i))
    
    # Some quick sanity checks
    for n in numbers:
        for i, c in enumerate(n.content):
            assert c.isdigit()
            assert grid.cell(n.x1 + i, n.y).content == c
        assert n.x2 - n.x1 + 1 == len(n.content), f"{n.content} {n.x1} {n.x2}"

    part_numbers = [n for n in numbers if n.is_part(grid)]
    total = sum((int(n.content) for n in part_numbers))
    # grid.print_grid(part_numbers)
    print(f"Count: {len(part_numbers)} parts, Sum: {total}")