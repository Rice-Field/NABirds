import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET
from PIL import Image
from PIL import ImageOps
import numpy as np
import scipy as sp
import os
import cv2

# crop BB from image
def cropface(image, BB):
	x0 = BB[0]
	y0 = BB[1]
	x2 = BB[2]
	y2 = BB[3]
	# target 4 has off image coordinates?
	return image[y0:y2, x0:x2, :]

# crop BB from image
def cropbird(image, BB):
	x0 = BB[0]
	y0 = BB[1]
	x2 = BB[0]+BB[2]
	y2 = BB[1]+BB[3]
	# target 4 has off image coordinates?
	return image[y0:y2, x0:x2, :]

# 48562 total images
face = np.loadtxt('bird_faces.txt', dtype=int) # face BB
# BB = np.loadtxt('bounding_boxes.txt', dtype=int, usecols = (1,2,3,4)) # bird BB
BB = np.loadtxt('bird_box.txt', dtype=int) # bird BB
dim = np.loadtxt('sizes.txt', dtype=int, usecols = (1,2)) # image size
ID = np.genfromtxt('images.txt',dtype='str') # image path

count = 0

for i in range(len(ID)):

	loc = ID[i][1]
	folder, name = loc.split('/')

	# face BB check
	if face[i][0] < 0 and face[i][0] != -999:
		count += 1
		print(name)
		print('face, negative x: %d' % (i+1))
	if face[i][1] < 0 and face[i][1] != -999:
		count += 1
		print(name)
		print('face, negative y: %d' % (i+1))
	if face[i][2] < 0 and face[i][2] != -999:
		count += 1
		print(name)
		print('face, negative x: %d' % (i+1))
	if face[i][3] < 0 and face[i][3] != -999:
		count += 1
		print(name)
		print('face, negative y: %d' % (i+1))

	if face[i][2] > dim[i][0]-1:
		count += 1
		print(name)
		print('face, x exceeds width: %d' % (i+1))
	if face[i][3] > dim[i][1]-1:
		count += 1
		print(name)
		print('face, y exceeds height: %d' % (i+1))

	# either bad data or bad calc
	if face[i][2] <= face[i][0] and face[i][0] != -999:
		count += 1
		print(name)
		print('face, minx > maxx: %d' % (i+1))
	if face[i][3] <= face[i][1] and face[i][0] != -999:
		count += 1
		print(name)
		print('face, miny > maxy: %d' % (i+1))

	# normalize
	# if face[i][0]/dim[i][0] > 1 or face[i][2]/dim[i][0] > 1:
	# 	print('face, x normalized: %d' % (i+1))
	# if face[i][1]/dim[i][1] > 1 or face[i][3]/dim[i][1] > 1:
	# 	print('face, x normalized: %d' % (i+1))


	x0 = BB[i][0]
	y0 = BB[i][1]
	x2 = BB[i][0] + BB[i][2]
	y2 = BB[i][1] + BB[i][3]

	# Bird BB check
	if x0 < 0:
		count += 1
		print((i+1))
		print('bird, negative x: %d' % (i+1))
	if y0 < 0:
		count += 1
		print((i+1))
		print('bird, negative y: %d' % (i+1))
	if x2 < 0:
		count += 1
		print((i+1))
		print('bird, negative x: %d' % (i+1))
	if y2 < 0:
		count += 1
		print((i+1))
		print('bird, negative y: %d' % (i+1))

	if x2 >= dim[i][0]:
		count += 1
		print((i+1))
		print('bird, x2: %d width: %d' % (x2, dim[i][0]))
		z = x2 - dim[i][0] + 1
		x2 = x2 - BB[i][2]
		BB[i][2] = BB[i][2] - z
		x2 = x2 + BB[i][2]
		print('new x2: %d' % (x2))

	if y2 >= dim[i][1]:
		count += 1
		print((i+1))
		print('bird, y2: %d height: %d' % (y2, dim[i][1]))
		z = y2 - dim[i][1] + 1
		y2 = y2 - BB[i][3]
		BB[i][3] = BB[i][3] - z
		y2 = y2 + BB[i][3]
		print('new y2: %d' % (y2))

	# either bad data or bad calc
	if x2 <= x0:
		count += 1
		print(name)
		print('bird, minx > maxx: %d' % (i+1))
	if y2 <= y0:
		count += 1
		print(name)
		print('bird, miny > maxy: %d' % (i+1))

	# normalize
	# if x0/dim[i][0] > 1 or x2/dim[i][0] > 1:
	# 	print('bird, x0: %g x2: %g' % (x0/dim[i][0], x2/dim[i][0]))
	# if y0/dim[i][1] > 1 or y2/dim[i][1] > 1:
	# 	print('bird, y0: %g y2: %g' % (y0/dim[i][1], y2/dim[i][1]))

	# print('')
print(count)

np.savetxt('bird_box.txt', BB, fmt='%d')