#!/usr/bin/env python3

import argparse
import json
import os
import sys

import lxml.etree as ET

class PageTree:
    def __init__(self, lines, source):
        self.root = ET.Element("xml")
        self.tree = ET.ElementTree(self.root)
        self.meta = ET.SubElement(self.root, "metadata")
        self.body = ET.SubElement(self.root, "body")
        self.source = ET.SubElement(self.meta, "source")
        self.source.text = source
        for n, line in enumerate(lines):
            if n == 0:
                elem = ET.SubElement(self.body, "headline")
            else:
                elem = ET.SubElement(self.body, "l")
            elem.set('n', str(n))
            elem.text = line
       
    def serialize(self, path):
        self.tree.write(path,
                        pretty_print=True, 
                        xml_declaration=True,
                        encoding='utf-8'
                        )

all_files = sys.argv

for f in all_files:
    with open(f, 'r') as handle:
        lines = [l.strip() for l in handle if l.strip() != ""]
    if lines is None:
        lines = []
    ptree = PageTree(lines, f)
    print(ET.tostring(ptree.root, pretty_print=True).decode())
