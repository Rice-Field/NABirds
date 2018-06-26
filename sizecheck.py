import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET
from PIL import Image
from PIL import ImageOps
import numpy as np
import scipy as sp
import os
import cv2

# crop BB from image
def crop(image, BB):
	x0 = BB[0]
	y0 = BB[1]
	x2 = BB[2]
	y2 = BB[3]
	# target 4 has off image coordinates?
	return image[y0:y2, x0:x2, :]

# 48562 total images
face = np.loadtxt('bird_faces.txt', dtype=int) # face BB
BB = np.loadtxt('bounding_boxes.txt', dtype=int, usecols = (1,2,3,4)) # bird BB
dim = np.loadtxt('sizes.txt', dtype=int, usecols = (1,2)) # image size
ID = np.genfromtxt('images.txt',dtype='str') # image path

count = 0
for i in range(len(ID)):
# for i in range(30300, 30308):
    print('image: %d' % i)

    if face[i][0] == -999:
        continue

    loc = ID[i][1]
    folder, name = loc.split('/')

    path = os.path.join('images', name)

    if not os.path.exists(path):
        continue

    image = Image.open(path).convert('RGB')
    width, height = image.size

    if width != dim[i][0]:
        print(path)
        count += 1

    if height != dim[i][1]:
        print(path)
        count += 1

print(count)