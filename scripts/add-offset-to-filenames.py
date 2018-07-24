#!/usr/bin/env python3

import yaml
import os

filesdir = '/Users/westgard/Desktop/NEH_INST/pipeline/ts_output/giles/'

with open('offsets.yml', 'r') as offsetsfile:
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
            source, vol, page = file.split('-')
            image, ext1, ext2 = page.split('.')
            if int(image) < int(v):
                offsetpage = 'a{0:03d}'.format(frontcounter)
                frontcounter += 1
            else:
                offsetpage = 'p{0:03d}'.format(pagecounter)
                pagecounter += 1
            
            newname = "{0}-{1}-{2}-{3}.{4}.{5}".format(
                source, vol, offsetpage, image, ext1, ext2
                )
            os.rename(os.path.join(volumedir, file), 
                      os.path.join(volumedir, newname)
                      )
