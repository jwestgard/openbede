#!/usr/bin/env python3

import argparse
import json
import os
import sys
import yaml
import lxml.etree as ET


REFERENCE = 'Giles 6.123-138'
DATA_HOME = '../data/ts_output/'
OFFSETS   = { 'v01': 176,   'v02': 6,   'v03': 10,  'v04': 27,
              'v05': 18,    'v06': 30,  'v07': 16,  'v08': 16,
              'v09': 18,    'v10': 20,  'v11': 16,  'v12': 18
              }


def get_files(citation, root, offsets):
    edition, ref = citation.split()
    edition = edition.lower()
    book, pagerange = ref.split('.')
    book = 'v{0:02d}'.format(int(book))
    offset = int(offsets[book])
    start, end = map(int, pagerange.split('-'))
    end += 1
    dir = os.path.join(root, edition)
    files = []
    for n in range(start, end):
        seq  = 's{0:03d}'.format(n+offset-1)
        page = 'p{0:03d}'.format(n)
        file = "{0}-{1}-{2}-{3}.png.txt".format(edition, book, page, seq)
        files.append(os.path.join(root, edition, book, file))
    return files


class Config():
    '''Class representing the configuration file for work generation'''
    def __init__(self, filepath):
        with open(filepath, 'r') as handle:
            self.works = yaml.load(handle)


class WorkTree:
    def __init__(self, files, source):
        self.root        = ET.Element("xml")
        self.tree        = ET.ElementTree(self.root)
        self.meta        = ET.SubElement(self.root, "metadata")
        self.source      = ET.SubElement(self.meta, "source")
        self.source.text = source
        self.body        = ET.SubElement(self.root, "body")
        for file in files:
            ed, bk, p, seq = os.path.basename(file).split('-')
            with open(file, 'r') as pagehandle:
                page = ET.SubElement(self.body, "page")
                page.set('n', "{0} {1}.{2}".format(ed.upper(), bk, p))
                lines = [line.strip() for line in pagehandle.readlines()]
                for ln, line in enumerate(lines):
                    if ln == 0:
                        elem = ET.SubElement(page, "headline")
                    else:
                        elem = ET.SubElement(page, "l")
                        elem.set('n', str(ln))
                        elem.text = line

    def serialize(self, path):
        self.tree.write(path, pretty_print=True, xml_declaration=True,
                        encoding='utf-8')
    
    def __str__(self):
        print(ET.tostring(wtree.root, pretty_print=True, encoding='utf8',
                          xml_declaration=True).decode())


def main():
    parser = argparse.ArgumentParser(
        description='Generate editions of works from OCR')
    parser.add_argument('-c', help='path to configuration')
    args = parser.parse_args()
    config = Config(args.c)
    all_works = config.works
    giles_works = [w for w in all_works.values() if "giles" in w['editions']]
    for w in giles_works:
        print(w['title'], w['editions']['giles'])
        


if __name__ == "__main__":
    main()
