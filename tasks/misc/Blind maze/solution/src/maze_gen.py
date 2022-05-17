#!/usr/bin/env python3

import numpy
from pyamaze import maze, agent
from PIL import Image

sign = lambda x: int(numpy.sign(x))


def get_value_from_cell_by_x_y(x, y, cell):
    assert(x < 3 and y < 3)
    if (x == 0 or x == 2) \
        and (y == 0 or y == 2):
        return 0

    if y == 1:
        if x == 0:
            return cell['W']
        elif x == 2:
            return cell['E']

    if x == 1:
        if y == 0:
            return cell['N']
        elif y == 1: # Center cell. Should be 1 if any side is open and 0 if all are closed
            return cell['N'] | cell['S'] | cell['E'] | cell['W']
        else:
            return cell['S']

    return 0


def map_to_bin_arr(maze_map, x = 8, y = 8):
    assert(x * y % 8 == 0)
    result = [0] * x * 3 * y * 3 # list with size x * y * 9
    for row in range(y * 3):
        for col in range(x * 3):
            result[row * (x * 3) + col] = get_value_from_cell_by_x_y(col % 3, row % 3, maze_map[(row // 3 + 1, col // 3 + 1)])

    return result


def bin_arr_to_bytes(bin_arr, x = 8, y = 8):
    assert(x * y % 8 == 0)
    bytes_arr = []
    curr_byte = 0
    byte_ctr = 0
    for row in range(y * 3):
        for col in range(x * 3):
            curr_byte |= bin_arr[row * x * 3 + col] << byte_ctr
            byte_ctr += 1

            if byte_ctr == 8:
                bytes_arr.append(curr_byte)
                byte_ctr = 0
                curr_byte = 0

    return bytes_arr


def print_arr(array):
    temp_arr = []
    for i in range(1, len(array) + 1):
        if i % 8 != 0:
            temp_arr.append(str(array[i - 1]))
        else:
            print(f"{', '.join(temp_arr)},")
            temp_arr.clear()
            temp_arr.append(str(array[i - 1]))
    if len(array) % 8 != 0:
        print(f"{', '.join(temp_arr)},")


if __name__ == '__main__':
    x = 24 # col count
    y = 24 # row count

    m = maze(y, x)
    m.CreateMaze()

    bin_arr = map_to_bin_arr(m.maze_map, x, y)
    bytes_arr = bin_arr_to_bytes(bin_arr, x, y)
    print_arr(bytes_arr)
    print(bytes_arr)

    img = Image.new('1', (x * 3, y * 3))
    pixels = img.load()

    arr = []

    for row in range(y * 3):
        for col in range(x * 3):
            img.putpixel((col, row), sign(bytes_arr[(row * (x * 3) + col) // 8] & (0x01 << ((row * (x * 3) + col) % 8))))
            arr.append(sign(bytes_arr[(row * (x * 3) + col) // 8] & (0x01 << ((row * (x * 3) + col) % 8))))

    img1 = img.resize((x * 50, y * 50))
    img1.show()

    m.run()
