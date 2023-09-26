import os
from PIL import Image
from array import array

fh = array('B')
for x in range(0,28):
    for y in range(0, 28):
        fh.append(0)
paths = [['/home/sqWang/liuliang/Train_png/0'],['/home/sqWang/liuliang/Train_png/1'],['/home/sqWang/liuliang/Test_png/0'],['/home/sqWang/liuliang/Test_png/1']]
for p in paths:
    for file in os.listdir(p[0]):
        tv = array('B')
        Im = Image.open(p[0] + '/' + file)
        pixel = Im.load()
        width, height = Im.size
        for x in range(0, width):
            for y in range(0, height):
                tv.append(pixel[x, y])
        if tv == fh:
            os.remove(p[0] + '/' + file)

