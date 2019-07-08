#!/usr/bin/env python3
# Copyright (C) 2018 t-r-a-g-e-d-y
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
import os
import random
import shutil
import subprocess
import sys

from PIL import Image, ImageDraw

def main(output_fn, block_size=48, rows=7, columns=7, padding=1, convert=True):
    width = block_size * (columns + padding * 2)
    height = block_size * (rows + padding * 2)

    bg = (228, 228, 228)
    fg = (random.randint(0,255), random.randint(0, 255), random.randint(0, 255))

    image = Image.new('RGB', (width, height), color=bg)
    draw = ImageDraw.Draw(image)

    def create_row():
        row = []
        for _ in range(columns // 2):
            row.append(random.randint(0, 1))

        if columns % 2 != 0:
            row.append(random.randint(0, 1))

        row += row[columns // 2 - 1::-1]
        return row

    indent = block_size * padding
    x = y = indent

    for row in range(rows):
        blocks = create_row()

        # I like the first and last rows to always be populated
        if row == 0 or row == rows - 1 and not any(blocks):
            while not any(blocks):
                blocks = create_row()

        for block in blocks:
            if block:
                rect = (x, y, x + block_size, y + block_size)
                draw.rectangle(rect, fill=fg)
            x += block_size

        x = indent
        y += block_size

    image.save(f'{output_fn}.png', format='PNG')
    if convert:
        convert_util(output_fn)

def convert_util(output_fn):
    # Windows has an unrelated convert.exe builtin
    if os.name != 'nt':
        target = 'convert'
        # the imagemagick convert utility cuts filesize by ~50%
        # by converting to mode P and reducing bit depth
        if shutil.which(target):
            subprocess.run([target, f'{output_fn}.png', f'{output_fn}.png'])

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(prog='pyvatar', description='Generate simple blocky avatars')

    parser.add_argument('outfile', help='Name of output file (no extension)')
    parser.add_argument('-r', default=7, metavar='n', type=int, help='Rows (Default: %(default)s)')
    parser.add_argument('-c', default=7, metavar='n', type=int, help='Columns (Default: %(default)s)')
    parser.add_argument('-p', default=1, metavar='n', type=int, help='Padding (Default: %(default)s)')
    parser.add_argument('-b', default=48, metavar='n', type=int, help=f'Block size (Default: %(default)s)')
    args = parser.parse_args()

    kwargs = {
        'rows':         args.r,
        'columns':      args.c,
        'padding':      args.p,
        'block_size':   args.b,
        'convert':      True
    }

    main(args.outfile, **kwargs)

