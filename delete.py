import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET
from PIL import Image
from PIL import ImageOps
import numpy as np
import scipy as sp
import os
import cv2
import glob

# 48562 total images
face = np.loadtxt('bird_faces.txt', dtype=int) # face BB
BB = np.loadtxt('bounding_boxes.txt', dtype=int, usecols = (1,2,3,4)) # bird BB
dim = np.loadtxt('sizes.txt', dtype=int, usecols = (1,2)) # image size
ID = np.genfromtxt('images.txt',dtype='str') # image path

# if not os.path.exists('images/'+'{}'.format(i).zfill(4)+'/'):
#     continue

count = 0
for filename in glob.glob('bad images/*.jpg'):
    fuld, nem = filename.split("\\")
    nim, typ = nem.split(".")
    os.remove('images/'+nem)
    os.remove('images/'+nim+'.xml')
    count += 1
    print(nem)
print(count)

# count = 0
# for filename in glob.glob('images/*.jpg'):
#     fuld, nem = filename.split("\\")
#     nim, typ = filename.split(".")
#     if not os.path.exists(nim+'.xml'):
#         count += 1
#         os.remove(filename)
#         print('deleting: '+nem)
# print(count)