#!/usr/bin/env python3

from wand.image import Image
import sys
import os

INPUT_PATH = sys.argv[1]
OUTPUT_ROOT = sys.argv[2]
EXT = 'png'
RESOLUTION = 300

def convert_pdf(original, output_dir, ext, resolution):
    print('Working on {}...'.format(original))
    pages = Image(filename=original, resolution=resolution)
    print('Source file has {} pages.'.format(len(pages)))
    for i, page in enumerate(pages.sequence, 1):
        print(' - Converting page {}'.format(i))
        with Image(page) as output:
            output.format = ext
            output.type = 'greyscale'
            base = os.path.splitext(os.path.basename(original))[0]
            filename = '{}-{}.{}'.format(base, i, ext)
            output_path = os.path.join(output_dir, filename)
            print(' - Writing to {}'.format(output_path))
            output.save(filename=output_path)

if os.path.isfile(INPUT_PATH):
    queue = [INPUT_PATH]
elif os.path.isdir(INPUT_PATH):
    queue = os.listdir(INPUT_PATH)

for source_file in queue:
    base = os.path.basename(source_file)
    output_dir = os.path.join(OUTPUT_ROOT)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    print('Converting {}'.format(source_file))
    convert_pdf(os.path.join(INPUT_PATH, source_file), 
                output_dir, 
                EXT,
                RESOLUTION
                )



