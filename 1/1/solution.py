#!/usr/bin/env python
from typing import List, Tuple

values: List[Tuple[int, int]] = []
with open('input.txt', 'r') as f:
    lines = f.readlines()
    for line in lines:
        digits = [d for d in line if d.isdigit()]
        assert digits
        values.append((digits[0], digits[-1]))
    assert(len(values) == len(lines))

total = sum((int(v[0] + v[1]) for v in values))
print(f"Count: {len(values)}, Sum: {total}")


    