# -*- coding:utf-8-unix -*-

from typing import Tuple
from PIL import Image
import sys



class Pixel:
    x = 0
    y = 0
    color = 0


class Group:
    index = 0
    color = None
    rightLeft = None
    rightRight = None
    downLeft = None
    downRight = None
    leftLeft = None
    leftRight = None
    UpLeft = None
    UpRight = None
    pixels = [] # type: list[Pixel]

groups = [] # type: list[Group]


def getExists(x: int, y: int):
    for g in groups:
        for p in g.pixels:
            if(p.x == x and p.y == y):
                return g
            if(p.x == x and p.y == y):
                return g
    return None


def searchPixel(x: int, y: int, img: Image, g: Group):
    if(x < 0 or x >= img.size[0]):
        return
    if(y < 0 or y >= img.size[1]):
        return
    if getExists(x, y):
        return
    pixel = Pixel()
    pixel.x = x
    pixel.y = y
    pixel.color = img.getpixel((x, y))
    if pixel.color == g.color:
        g.pixels.append(pixel)
        searchPixel(x-1, y, img, g)
        searchPixel(x+1, y, img, g)
        searchPixel(x, y-1, img, g)
        searchPixel(x, y+1, img, g)


def calcGroup():
    for g in groups:
        xs = [p.x for p in g.pixels]
        ys = [p.y for p in g.pixels]
        g.rightLeft = min(filter(lambda p: p.x == max(xs), g.pixels), key=lambda p: p.y)
        g.rightRight = max(filter(lambda p: p.x == max(xs), g.pixels), key=lambda p: p.y)
        g.downLeft = max(filter(lambda p: p.y == max(ys), g.pixels), key=lambda p: p.x)
        g.downRight = min(filter(lambda p: p.y == max(ys), g.pixels), key=lambda p: p.x)
        g.leftLeft = max(filter(lambda p: p.x == min(xs), g.pixels), key=lambda p: p.y)
        g.leftRight = min(filter(lambda p: p.x == min(xs), g.pixels), key=lambda p: p.y)
        g.upLeft = min(filter(lambda p: p.y == min(ys), g.pixels), key=lambda p: p.x)
        g.upRight = max(filter(lambda p: p.y == min(ys), g.pixels), key=lambda p: p.x)


def printGroup(w: int, h: int):
    for g in groups:
        hue, lightness = getColor(g.color)
        print("{0},{1}".format(hue, lightness), end="")
        for p in [g.rightLeft, g.rightRight, g.downLeft, g.downRight, g.leftLeft, g.leftRight, g.upLeft, g.upRight]:
            print(",{0}{1}".format(toColumn(p.x), p.y + 2), end="")
        print(",{0}".format(len(g.pixels)))
    for j in range(h):
        for i in range(w):
            e = getExists(i, j)
            print(",A{0}".format(e.index + 50), end="")
        print()


def getColor(c: Tuple):
    # black
    if c == (0, 0, 0):
        return (-1, -1)
    # white
    elif c == (0xff, 0xff, 0xff):
        return (6, 6)
    # red
    elif c == (0xff, 0xc0, 0xc0):
        return (0, 2)
    elif c == (0xff, 0x00, 0x00):
        return (0, 1)
    elif c == (0xc0, 0x00, 0x00):
        return (0, 0)
    # yellow
    elif c == (0xff, 0xff, 0xc0):
        return (1, 2)
    elif c == (0xff, 0xff, 0x00):
        return (1, 1)
    elif c == (0xc0, 0xc0, 0x00):
        return (1, 0)
    # green
    elif c == (0xc0, 0xff, 0xc0):
        return (2, 2)
    elif c == (0x00, 0xff, 0x00):
        return (2, 1)
    elif c == (0x00, 0xc0, 0x00):
        return (2, 0)
    # cyan
    elif c == (0xc0, 0xff, 0xff):
        return (3, 2)
    elif c == (0x00, 0xff, 0xff):
        return (3, 1)
    elif c == (0x00, 0xc0, 0xc0):
        return (3, 0)
    # blue
    elif c == (0xc0, 0xc0, 0xff):
        return (4, 2)
    elif c == (0x00, 0x00, 0xff):
        return (4, 1)
    elif c == (0x00, 0x00, 0xc0):
        return (4, 0)
    # magenta
    elif c == (0xff, 0xc0, 0xff):
        return(5, 2)
    elif c == (0xff, 0x00, 0xff):
        return (5, 1)
    elif c == (0xc0, 0x00, 0xc0):
        return (5, 0)
    # error
    else:
        return (128, 128)

def toColumn(x: int):
    return "{0}{1}".format("" if x <= 26 else chr(65 + x / 26), chr(66 + x % 26))


def main():
    img = Image.open(sys.argv[1])
    for j in range(img.size[1]):
        for i in range(img.size[0]):
            pixel = Pixel()
            pixel.x = i
            pixel.y = j
            pixel.color = img.getpixel((i, j)) 
            if getExists(i, j):
                continue
            else:
                g = Group()
                g.color = pixel.color
                g.pixels = [pixel]
                g.index = len(groups)
                groups.append(g)
                if g.color != (0xff, 0xff, 0xff):
                    searchPixel(i-1, j, img, g)
                    searchPixel(i+1, j, img, g)
                    searchPixel(i, j-1, img, g)
                    searchPixel(i, j+1, img, g)
    calcGroup()
    printGroup(img.size[0], img.size[1])




if __name__ == "__main__":
    main()
