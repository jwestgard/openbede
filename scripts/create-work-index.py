#!/usr/bin/env python3

import yaml
import sys

with open(sys.argv[1], 'r') as inputfile:
    data = yaml.load(inputfile)

for work in data:
    data[work]['abbreviation'] = work

with open(sys.argv[2], 'w') as outputfile:
    yaml.dump(data, 
              outputfile, 
              default_flow_style=False,
              indent=2
              )
