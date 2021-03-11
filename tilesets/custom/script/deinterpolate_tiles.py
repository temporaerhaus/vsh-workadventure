#!/usr/bin/env python3

"""
Workaround script for WorkAdventure interpolation problems:
Inserts an empty row below each row of tiles

Usage: python deinterpolate_tiles.py tileset.png tileset_new.png

Requires: Pillow (pip install Pillow)

Only apply this script to tilesets that haven't been used in the map yet!

Modified script from https://github.com/c3CERT/rc3_tiles
License: CC-BY-SA - CERT (cert.ccc.de)

"""


from PIL import Image
import sys
import os

BASE_DIR = os.getcwd()
SOURCE_FILENAME = sys.argv[1]
RESULT_FILENAME = sys.argv[2]

IMG = Image.open(SOURCE_FILENAME)
TILESHEET_WIDTH, TILESHEET_HEIGTH = IMG.size


class Row():
    def __init__(self, width=TILESHEET_WIDTH, height=32):
        self.width = width
        self.height = height
        self.remainingWidth = width
        self.sprites = []

    def append(self, Img):
        x, y = Img.size
        if (self.remainingWidth - x) < 0:
            raise Exception('ImageTooLarge')
        self.height = max(self.height, y)
        if self.height > TILESHEET_HEIGTH:
            raise Exception("Tilesheet full")
        self.remainingWidth = self.remainingWidth - x
        self.sprites.append(Img.convert(mode='RGBA'))
        return self.remainingWidth

    def render(self):
        row = Image.new('RGBA', (self.width, self.height), (255, 255, 255, 0))
        x_offset = 0
        for img in self.sprites:
            x, y = img.size
            row.alpha_composite(img, (x_offset, 0))
            x_offset += x
        return row


class Spritesheet():
    def __init__(self, width=TILESHEET_WIDTH, height=TILESHEET_HEIGTH):
        self.width = width
        self.height = height
        self.rows = []

    def append(self, Img):
        x, y = Img.size
        self.rows.append(Img)

    def render(self):
        sheet = Image.new('RGBA', (self.width, self.height),
                          (255, 255, 255, 0))
        y_offset = 0
        for img in self.rows:
            x, y = img.size
            sheet.alpha_composite(img, (0, y_offset))
            y_offset += y
        return sheet


sheet = Spritesheet()

for i in range(0, int(TILESHEET_HEIGTH / 32) - 1):
    row = Row()
    tiles = IMG.crop(
        (0, i * 32, TILESHEET_WIDTH, (i + 1) * 32))
    row.append(tiles)
    sheet.append(row.render())
    sheet.append(Row().render())

sheet.render().save(RESULT_FILENAME)
