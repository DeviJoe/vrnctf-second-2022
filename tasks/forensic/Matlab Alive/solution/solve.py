from scipy.io import loadmat
import cv2

imgs = loadmat('images.mat')

for i, im in enumerate(imgs['im']):
    cv2.imwrite("imgs/img" + str(i) + ".png", im)

# затем внимательно посмотрите файлы, на одной картинке написан флаг