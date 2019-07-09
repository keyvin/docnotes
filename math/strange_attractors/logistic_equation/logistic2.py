#!/usr/bin/python3

import os
from PIL import *
from PIL import Image,ImageDraw


img_sizex = 1000
img_sizey = 1000




###plot logistic diagram, r= 3.25
ic = .3
r = 4
results = []

iter = 10000

x = ic
xnew = ic
while iter:

    results.append((int(x*1000), int(xnew*1000)))
    x = xnew
    xnew = r * x *(1-x)
    iter = iter -1


    img = Image.new("RGB", (img_sizex, img_sizey)) 
draw = ImageDraw.Draw(img)
xy = ((10, 10), (11, 11), (12, 12))
draw.point(results, fill=None)
print(results[1:100])
img.save("img.png", "PNG")

os.system("lximage-qt img.png")
