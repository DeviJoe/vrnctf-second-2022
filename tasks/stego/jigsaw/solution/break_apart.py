from PIL import Image
import random

from utils import *

N = 16
name = 'solution.png'

im = Image.open(name)
imgwidth, imgheight = im.size
height = imgheight // N
width = imgwidth // N

l = range(0, 32768)
borders = random.sample(l, k=height * (width - 1) + (height - 1) * width)
borders_h = borders[:height * (width - 1)]
borders_w = borders[height * (width - 1):]

borders_h = split_list(borders_h, height)
borders_w = split_list(borders_w, height - 1)

images = []

for i in range(height):
    images_w = []
    for j in range(width):
        box = (j * N, i * N, (j + 1) * N, (i + 1) * N)
        new_im = Image.new('RGB', (N + 2, N + 2), (255, 255, 255))
        a = im.crop(box)
        new_im.paste(a, (1, 1))
        images_w.append(new_im)

    images.append(images_w)

names = list(range(width*height))

print(width*height)

for i in range(height):
    for j in range(width):
        image = images[i][j]
        up = down = left = right = 0
        if i != 0:
            up = borders_w[i - 1][j]
        if i != height - 1:
            down = borders_w[i][j]
        if j != 0:
            left = borders_h[i][j - 1]
        if j != width - 1:
            right = borders_h[i][j]
        put_borders(image, up, left, down, right)
        print(i * width + j)
        name = random.choice(names)
        names.remove(name)
        image.save("images/" + str(name) + '.png')


