from enum import Enum
from PIL import Image


class Border(Enum):
    UP = 1
    LEFT = 2
    RIGHT = 3
    DOWN = 4


def split_list(alist, wanted_parts=1):
    length = len(alist)
    return [alist[i * length // wanted_parts: (i + 1) * length // wanted_parts] for i in range(wanted_parts)]


def put_border(image: Image, value, t):
    if value == 0:
        return
    black = (0, 0, 0)
    white = (255, 255, 255)
    val = f'{value:>016b}'
    if t == Border.UP:
        for i in range(len(val)):
            if val[i] == '0':
                image.putpixel((1 + i, 0), white)
            else:
                image.putpixel((1 + i, 0), black)
    elif t == Border.DOWN:
        for i in range(len(val)):
            if val[i] == '0':
                image.putpixel((1 + i, 17), black)
            else:
                image.putpixel((1 + i, 17), white)
    elif t == Border.LEFT:
        for i in range(len(val)):
            if val[i] == '0':
                image.putpixel((0, 1 + i), white)
            else:
                image.putpixel((0, 1 + i), black)
    elif t == Border.RIGHT:
        for i in range(len(val)):
            if val[i] == '0':
                image.putpixel((17, 1 + i), black)
            else:
                image.putpixel((17, 1 + i), white)


def put_borders(image, border_up, border_left, border_down, border_right):
    put_border(image, border_up, Border.UP)
    put_border(image, border_left, Border.LEFT)
    put_border(image, border_down, Border.DOWN)
    put_border(image, border_right, Border.RIGHT)
