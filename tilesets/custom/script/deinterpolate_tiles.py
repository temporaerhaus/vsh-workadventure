#!/usr/bin/env python3

"""
Workaround script for WorkAdventure interpolation problems

Usage: python deinterpolate_tiles.py tileset.png tileset_new.png

Requires: Pillow (pip install Pillow)

Only apply this script to tilesets that haven't been used in the map yet!

Modified script from https://github.com/c3CERT/rc3_tiles
License: CC-BY-SA - CERT (cert.ccc.de)

"""


from PIL import Image
import sys
import os

TILE_SIZE = 32
BASE_DIR = os.getcwd()
SOURCE_FILENAME = sys.argv[1]
RESULT_FILENAME = sys.argv[2]

IMG = Image.open(SOURCE_FILENAME)
TILESHEET_WIDTH, TILESHEET_HEIGHT = IMG.size


class Row():
    def __init__(self, width=TILESHEET_WIDTH * 2 + 64, height=TILE_SIZE):
        self.width = width
        self.height = height
        self.remainingWidth = width
        self.sprites = []

    def append(self, Img):
        x, y = Img.size
        if (self.remainingWidth - x) < 0:
            pass #raise Exception('ImageTooLarge')
        self.height = max(self.height, y)
        if self.height > TILESHEET_HEIGHT:
            pass #raise Exception("Tilesheet full")
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
    def __init__(self, width=TILESHEET_WIDTH * 2 + 64, height=TILESHEET_HEIGHT * 2  + 64):
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

sheet.append(Row(height=1).render())

for i in range(0, TILESHEET_HEIGHT - 32, 32):

    tiles = Row()
    top_border = Row(height=1)
    bottom_border = Row(height=1)

    tiles.append(Image.new('RGBA', (1, 32), (0, 0, 0, 0)))

    for j in range(0, TILESHEET_WIDTH - 32, 32):
        top_border.append(Image.new('RGBA', (32, 1), (0, 0, 0, 0)))
        bottom_border.append(Image.new('RGBA', (32, 1), (0, 0, 0, 0)))

        top_border.append(IMG.crop((j, i, j + 32, i + 1)))
        bottom_border.append(IMG.crop((j, i + 31, j + 32, i + 32)))

        tiles.append(Image.new('RGBA', (30, 32), (0, 0, 0, 0)))
        tiles.append(IMG.crop((j, i, j + 1, i + 32)))
        tiles.append(IMG.crop((j, i, j + 32, i + 32)))
        tiles.append(IMG.crop((j + 31, i, j + 32, i + 32)))

    top_border.append(Image.new('RGBA', (32, 1), (0, 0, 0, 0)))
    bottom_border.append(Image.new('RGBA', (32, 1), (0, 0, 0, 0)))
    tiles.append(Image.new('RGBA', (31, 32), (0, 0, 0, 0)))


    sheet.append(Row(height=30).render())
    sheet.append(top_border.render())
    sheet.append(tiles.render())
    sheet.append(bottom_border.render())

sheet.append(Row(height=31).render())

sheet.render().save(RESULT_FILENAME)
