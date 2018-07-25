#!/usr/bin/env python3

import yaml
import os

filesdir = '/Users/westgard/Dev/openbede/data/ts_output/giles'

with open('../config/edition-offsets-giles.yml', 'r') as offsetsfile:
    offsets = yaml.load(offsetsfile)

for k,v in offsets.items():
    frontcounter = 1
    pagecounter = 1
    volumedir = os.path.join(filesdir, k)
    allfiles = sorted(os.listdir(volumedir))
    for file in allfiles:
        if file.startswith('.'):
            continue
        else:
            source, vol, page, seqext = file.split('-')
            seq, iext, fext = seqext.split('.')
            seq = int(seq.lstrip('s'))
            if int(seq) < int(v):
                offsetpage = 'a{0:03d}'.format(frontcounter)
                frontcounter += 1
            else:
                offsetpage = 'p{0:03d}'.format(pagecounter)
                pagecounter += 1
            seq = 's{0:03d}'.format(seq)
            newname = '{0}-{1}-{2}-{3}.{4}.{5}'.format(
                source, vol, offsetpage, seq, iext, fext
                )
            print("moving {} to {}".format(file, newname))
            os.rename(os.path.join(volumedir, file), 
                      os.path.join(volumedir, newname)
                      )
