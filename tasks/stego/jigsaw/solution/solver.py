#!/usr/bin/env python3

from PIL import Image
from os import listdir
from os.path import isfile, join
from enum import IntEnum

class Border(IntEnum):
    CENTER = 0
    LEFT = 1
    RIGHT = 2
    TOP = 4
    BOTTOM = 8
    MASK = 15


border_color = 255 * 3


def get_img_type(img: Image.Image):
    img_type = Border.MASK

    for idx in range(img.width):
        if sum(img.getpixel((idx, 0))) != border_color:
            img_type &= ~Border.TOP

        if sum(img.getpixel((idx, img.height - 1))) != border_color:
            img_type &= ~Border.BOTTOM

    for idx in range(img.height):
        if sum(img.getpixel((0, idx))) != border_color:
            img_type &= ~Border.LEFT

        if sum(img.getpixel((img.width - 1, idx))) != border_color:
            img_type &= ~Border.RIGHT

    return img_type


def compute_width_and_height(img_list: list[Image.Image]):
    width = 0
    height = 0

    for img in img_list:
        img_type = get_img_type(img)

        if (img_type & Border.TOP or img_type & Border.BOTTOM):
            width += 1

        if (img_type & Border.LEFT or img_type & Border.RIGHT):
            height += 1

    return width // 2, height // 2


def get_mask(img: Image.Image, border: Border):
    mask = 0

    if border == Border.CENTER:
      return None

    if border & Border.TOP or border & Border.BOTTOM:
        for idx in range(1, img.width - 1):
            if border & Border.TOP:
                mask |= int(sum(img.getpixel((idx, 0))) == border_color) << idx

            elif border & Border.BOTTOM:
                mask |= int(sum(img.getpixel((idx, img.height - 1))) == border_color) << idx

    if border & Border.LEFT or border & Border.RIGHT:
        for idx in range(1, img.height - 1):
            if border & Border.LEFT:
                mask |= int(sum(img.getpixel((0, idx))) == border_color) << idx

            elif border & Border.RIGHT:
                mask |= int(sum(img.getpixel((img.height - 1, idx))) == border_color) << idx

    return mask >> 1


def find_pair(img: Image.Image, img_list: list[Image.Image], direction: Border):
    if direction == Border.CENTER:
        return None

    original_mask = get_mask(img, direction)

    if direction & Border.TOP or direction & Border.BOTTOM:
        target_mask = ~get_mask(img, direction) & ((1 << img.width - 2) - 1)
    else:
        target_mask = ~get_mask(img, direction) & ((1 << img.height - 2) - 1)

    opposite_direction = 0

    result = None

    if direction & Border.TOP:
        opposite_direction |= Border.BOTTOM
    elif direction & Border.BOTTOM:
        opposite_direction |= Border.TOP
    elif direction & Border.LEFT:
        opposite_direction |= Border.RIGHT
    else:
        opposite_direction |= Border.LEFT


    for pair in img_list:
        mask = get_mask(pair, opposite_direction)
        if target_mask == mask:
            result = pair
            break

    return result


def solve_line(img_list: list[Image.Image], width: int, first_img_on_prev_line: Image.Image = None):
    line = []

    if not first_img_on_prev_line:
        curr_img = None
        for img in img_list:
            curr_img_type = get_img_type(img)

            if curr_img_type & Border.TOP and curr_img_type & Border.LEFT:
                line.append(img)
                first_img_on_prev_line = img
                break

        if (curr_img):
            img_list.remove(curr_img)

    while len(line) < width:
        if len(line) == 0:
            curr_img = find_pair(first_img_on_prev_line, img_list, Border.BOTTOM)
        else:
            curr_img = find_pair(line[-1], img_list, Border.RIGHT)

        if curr_img:
            img_list.remove(curr_img)
            line.append(curr_img)
        else:
            break

    return line


def solve(img_list: list[Image.Image]):
    width, height = compute_width_and_height(img_list)
    prev_line = []
    result_img = Image.new(img_list[0].mode, (width * (img_list[0].width - 2), height * (img_list[0].height - 2)))

    prev_line = solve_line(img_list, width)
    first_img_on_prev_line = prev_line[0]

    for idx, img in enumerate(prev_line):
        result_img.paste(img.crop((1, 1, img.width - 1, img.height - 1)), (idx * (img.width - 2), 0))

    result_img.save("result.png")

    for row in range(1, height):
        prev_line = solve_line(img_list, width, first_img_on_prev_line)

        first_img_on_prev_line = prev_line[0]

        for idx, img in enumerate(prev_line):
            result_img.paste(img.crop((1, 1, img.width - 1, img.height - 1)), (idx * (img.width - 2), row * (img.height - 2)))

        result_img.save("result.png")

    first_img_on_prev_line.close()



if __name__ == "__main__":
    path = "images"
    img_list = [Image.open(join(path, f)).convert('RGB') for f in listdir(path) if isfile(join(path, f))]
    solve(img_list)