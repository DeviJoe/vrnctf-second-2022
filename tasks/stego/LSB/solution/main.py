from math import log
import random
import cv2
import numpy as np


def read_file(filename):
    with open(filename, 'r') as file:
        return file.read()


def save(text, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(text)


def steghide(img, text):
    im = np.copy(img)
    h, w, k = im.shape
    cx = 0
    cy = 0
    tx = text + '\0'
    for c in tx:
        t = ord(c)
        for i in range(8):
            if t % 2 != im[cx][cy][1] % 2:
                im[cx][cy][1] = im[cx][cy][1] ^ 1
            t = t >> 1
            cy += 1
            if cy + 1 > h:
                cy = 0
                cx += 1

    return im


def stegget(img):
    h, w, k = img.shape
    cx = 0
    cy = 0
    a = ""
    while (True):
        t = 0
        for i in range(8):
            if img[cx][cy][1] % 2 == 1:
                t += 1 << i
            cy += 1
            if cy + 1 > h:
                cy = 0
                cx += 1
        if t == 0:
            break
        a += chr(t)
    return a


if __name__ == "__main__":
    im = cv2.imread("vova_hide.bmp")
    print("Hidden text:", stegget(im))

