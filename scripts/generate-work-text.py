#!/usr/bin/env python3

import argparse
import json
import os
import sys
import yaml
import lxml.etree as ET


DATA_HOME = 'data/ts_output/'
XML_OUT   = 'edition'
HTML_OUT  = 'docs'
OFFSETS   = { 'v01': 176,   'v02': 6,   'v03': 10,  'v04': 27,
              'v05': 18,    'v06': 30,  'v07': 16,  'v08': 16,
              'v09': 18,    'v10': 20,  'v11': 16,  'v12': 18
              }


def get_files(edition, blocks, root, offsets):
    result = []
    odd = False
    even = False
    for block in blocks.split(','):
        if ' (odd)' in block:
            odd = True
            block = block.replace(' (odd)', '')
        elif ' (even)' in block:
            even = True
            block = block.replace(' (odd)', '')
        book, pagerange = block.split('.')
        book = 'v{0:02d}'.format(int(book))
        offset = int(offsets[book])
        if '-' in pagerange:
            start, end = map(int, pagerange.split('-'))
        else:
            start = end = int(pagerange)
        end += 1
        dir = os.path.join(root, edition)
        if odd:
            pagenums = [n for n in range(start, end) if n%2 == 1]
        elif even:
            pagenums = [n for n in range(start, end) if n%2 == 0]
        else:
            pagenums = range(start, end)
        for n in range(start, end):
            seq  = 's{0:03d}'.format(n+offset-1)
            page = 'p{0:03d}'.format(n)
            file = "{0}-{1}-{2}-{3}.png.txt".format(edition, book, page, seq)
            result.append(os.path.join(root, edition, book, file))
    return result


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
        print(ET.tostring(self.root, pretty_print=True, encoding='utf8',
                          xml_declaration=True).decode())


class HTMLTree:
    def __init__(self, files, source):
        self.root        = ET.Element("xhtml")
        self.tree        = ET.ElementTree(self.root)
        self.head        = ET.SubElement(self.root, "head")
        
        meta = ET.SubElement(self.head, "meta", 
                             charset = 'utf-8', 
                             )
        link = ET.SubElement(self.head, "link", 
                             rel = 'stylesheet',         
                             type = 'text/css', 
                             href = 'css/stylesheet.css'
                             )
        
        self.source      = ET.SubElement(self.head, "title")
        self.source.text = source
        self.body        = ET.SubElement(self.root, "body")
        self.pageframe   = ET.SubElement(self.body, "div", id = "page-frame")
        self.mainframe   = ET.SubElement(self.pageframe, "div", 
                                         id = "main-frame"
                                         )
        self.maintext    = ET.SubElement(self.mainframe, "div", 
                                         id = "main-text"
                                         )
        for file in files:
            ed, bk, p, seq = os.path.basename(file).split('-')
            with open(file, 'r') as pagehandle:
                para = ET.SubElement(self.maintext, "p")
                lines = [line.strip() for line in pagehandle.readlines()]
                para.text = ''
                for ln, line in enumerate(lines):
                    if ln == 0:
                        pass
                    else:
                        if line.endswith('-'):
                            line = line[:-1]
                        para.text = para.text + line
                            
                        
    def serialize(self, path):
        self.tree.write(path, pretty_print=True, xml_declaration=True,
                        encoding='utf-8')



def main():
    parser = argparse.ArgumentParser(
        description='Generate editions of works from OCR')
    parser.add_argument('-c', help='path to configuration')
    args = parser.parse_args()
    config = Config(args.c)
    all_works = config.works
    for abbrev,work in all_works.items():
        if work['editions'] == "None":
            continue
        else:
            print(abbrev, work['title'], work['editions'])
            for edition, blocks in work['editions'].items():
                files = get_files(edition, blocks, DATA_HOME, OFFSETS)
                citation = "{0}, {1}".format(edition.upper(), blocks)
                xml = WorkTree(files, citation)
                xml.serialize(os.path.join(XML_OUT, (abbrev + '.xml')))
                html = HTMLTree(files, citation)
                html.serialize(os.path.join(HTML_OUT, (abbrev + '.html')))

if __name__ == "__main__":
    main()
