#!/usr/bin/env python
from typing import List, Tuple
import re

# quick grep of the input didn't find any "teen", "ty", "ten", "eleven", "twelve", "hundred", "etc"
# visual scan also revealed crafty word combos that would be hard to regex:
#   eightwo, threeight, etc
words = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
values: List[Tuple[int, int]] = []
with open('input.txt', 'r') as f:
    lines = f.readlines()
    for line in lines:
        seq = []
        for i, val in enumerate(line):
            if val.isdigit():
                seq.append(val)
            else:
                for w in words:
                    if line[i:-1].startswith(w):
                        seq.append(w)
                        break          

        first, last = seq[0], seq[-1]
        values.append((int(first) if first.isdigit() else words.index(first),
                       int(last) if last.isdigit() else words.index(last)))

        print(values[-1], seq, line.strip())
    assert(len(values) == len(lines))

total = sum((int(str(v[0]) + str(v[1])) for v in values))
print(f"Count: {len(values)}, Sum: {total}")

