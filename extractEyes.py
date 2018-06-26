import matplotlib.pyplot as plt
from PIL import Image
from PIL import ImageOps
import numpy as np
import scipy as sp
import tensorflow as tf
import os
import cv2

Parts = np.loadtxt('parts/part_locs.txt', usecols = (1,2,3,4))
# 48562 total images
ID = np.genfromtxt('images.txt',dtype='str')

eyes = np.zeros([48562, 7], dtype=int)

j = 0
for i in range(len(Parts)):
	# filename = os.path.join(r'images',ID[i][1])
	# print('image %d' % (i+1))

	if Parts[i][0] == 3:
		eyes[j][0] = j+1
		eyes[j][1] = Parts[i][1]
		eyes[j][2] = Parts[i][2]
		eyes[j][3] = Parts[i][3]

	if Parts[i][0] == 4:
		eyes[j][4] = Parts[i][1]
		eyes[j][5] = Parts[i][2]
		eyes[j][6] = Parts[i][3]
		j += 1

np.savetxt('eye_loc.txt', eyes, fmt='%d')
