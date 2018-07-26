#!/usr/bin/env python3

import os
import sys

INPUT_DIR = sys.argv[1]
COLLATION = sys.argv[2]

def expand_collation_string(collation):
    f, p, b      = collation.split(';')
    front_matter = int(f.replace(' ','').replace('a',''))
    back_matter  = int(b.replace(' ','').replace('z',''))
    page_ranges  = p.replace(' ','').replace('p','').split(',')
    page_nos = []
    page_nos.extend(
        ['a{0:03d}'.format(n) for n in range(1, front_matter + 1)]
        ) 
    for block in page_ranges:
        start, end = map(int, block.split('-'))
        page_nos.extend(
            ['p{0:03d}'.format(n) for n in range(start, end + 1)]
            )
    page_nos.extend(
        ['z{0:03d}'.format(n) for n in range(1, back_matter + 1)]
        )
    return page_nos


page_nos = expand_collation_string(COLLATION)
files = sorted([f for f in os.listdir(INPUT_DIR) if not f.startswith('.')])
serial_nos = ['s{0:03d}'.format(n) for n in range(1, len(files) + 1)]
collation_map = [t for t in zip(serial_nos, page_nos)]

for file in files:
    pref = '-'.join(file.split('-')[:2])
    exts = '.'.join(file.split('.')[1:])
    ser_no, page_no = collation_map.pop(0)
    os.rename(file, "{0}-{1}-{2}.{3}".format(pref, page_no, ser_no, exts))
