#!/usr/bin/env python3

import os
import yaml

REFERENCE = 'Giles 6.128-151'
DATA_HOME = '../data'

def getWorkFiles(citation, root):
    edition, ref = citation.split()
    edition = edition.lower()
    book, pagerange = ref.split('.')
    start, end = map(int, pagerange.split('-'))
    dir = os.path.join(root, edition)
    files = []
    for n in range(start, end):
        file = "{0}-v{1}-p{2}-s{3}.png.txt".format(edition, book, n, n)
        files.append(file)
    return files

print(getWorkFiles(REFERENCE, DATA_HOME))
