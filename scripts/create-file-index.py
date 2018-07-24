#!/usr/bin/env python3

import csv
import os
import sys

ROOT = sys.argv[1]
OUTPUT = sys.argv[2]

class PageImg(dict):
    def __init__(self, path, root):
        self.fullpath = os.path.join(root, path)
        self.relpath = os.path.relpath(self.fullpath, root)
        self.filename = os.path.basename(path)
        self.source, self.v, self.p, self.extsec = self.filename.split('-')
        self.s, self.e1, self.e2 = self.extsec.split('.')

with open(OUTPUT, 'w') as outhandle:
    fieldnames = ['source', 'v', 'p', 's', 'relpath']
    writer = csv.DictWriter(outhandle, 
                            fieldnames=fieldnames, 
                            extrasaction='ignore')
    writer.writeheader()
    for root, dir, files in os.walk(ROOT):
        for f in files:
            if f.endswith('.txt') and not f.startswith('.'):
                row = PageImg(f, ROOT)
                writer.writerow(row.__dict__)
    
