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
	x2 = BB[0]+BB[2]
	y2 = BB[1]+BB[3]
	# target 4 has off image coordinates?
	return image[y0:y2, x0:x2, :]

# 48562 total images
face = np.loadtxt('bird_faces.txt', dtype=int) # face BB
BB = np.loadtxt('bounding_boxes.txt', dtype=int, usecols = (1,2,3,4)) # bird BB
dim = np.loadtxt('sizes.txt', dtype=int, usecols = (1,2)) # image size
ID = np.genfromtxt('images.txt',dtype='str') # image path

for i in range(len(ID)):
	print('image: %d' % (i+1))

	loc = ID[i][1]
	folder, name = loc.split('/')

	path = os.path.join('images', loc)
	image = Image.open(path).convert('RGB')

	im = Image.fromarray(crop(np.asarray(image), BB[i]))
	im.save('birds/'+name)
	continue
