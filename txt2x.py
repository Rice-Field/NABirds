import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET
from PIL import Image
from PIL import ImageOps
import numpy as np
import scipy as sp
import os
import cv2

# 48562 total images
face = np.loadtxt('bird_faces.txt', dtype=int) # face BB
# BB = np.loadtxt('bounding_boxes.txt', dtype=int, usecols = (1,2,3,4)) # bird BB
BB = np.loadtxt('bird_box.txt', dtype=int)
dim = np.loadtxt('sizes.txt', dtype=int, usecols = (1,2)) # image size
ID = np.genfromtxt('images.txt',dtype='str') # image path

for i in range(len(ID)):
    print('image: %d' % (i+1))
    anno = ET.Element('annotation')
    Tree = ET.ElementTree(element=anno)

    word = ID[i][1]
    fuld, nem = word.split('/')

    # face is present
    if face[i][0] != -999:
        folder = ET.SubElement(anno, 'folder')
        folder.text = ''
        filename = ET.SubElement(anno, 'filename')
        filename.text = nem
        path = ET.SubElement(anno, 'path')
        path.text = nem

        source = ET.SubElement(anno, 'source')
        database = ET.SubElement(source, 'database')
        database.text = 'Unknown'

        size = ET.SubElement(anno, 'size')
        width = ET.SubElement(size, 'width')
        width.text = str(dim[i][0])
        height = ET.SubElement(size, 'height')
        height.text = str(dim[i][1])
        depth = ET.SubElement(size, 'depth')
        depth.text = str(3)

        segmented = ET.SubElement(anno, 'segmented')
        segmented.text = str(0)

        obj = ET.SubElement(anno, 'object')
        name = ET.SubElement(obj, 'name')
        name.text = 'bird'
        pose = ET.SubElement(obj, 'pose')
        pose.text = 'Unspecified'
        truncated = ET.SubElement(obj, 'truncated')
        truncated.text = str(0)
        difficult = ET.SubElement(obj, 'difficult')
        difficult.text = str(0)
        bndbox = ET.SubElement(obj, 'bndbox')
        xmin = ET.SubElement(bndbox, 'xmin')
        xmin.text = str(BB[i][0])
        ymin = ET.SubElement(bndbox, 'ymin')
        ymin.text = str(BB[i][1])
        xmax = ET.SubElement(bndbox, 'xmax')
        xmax.text = str(BB[i][0]+BB[i][2])
        ymax = ET.SubElement(bndbox, 'ymax')
        ymax.text = str(BB[i][1]+BB[i][3])

        obj2 = ET.SubElement(anno, 'object')
        name2 = ET.SubElement(obj2, 'name')
        name2.text = 'bird_face'
        pose2 = ET.SubElement(obj2, 'pose')
        pose2.text = 'Unspecified'
        truncated2 = ET.SubElement(obj2, 'truncated')
        truncated2.text = str(0)
        difficult2 = ET.SubElement(obj2, 'difficult')
        difficult2.text = str(0)
        bndbox2 = ET.SubElement(obj2, 'bndbox')
        xmin2 = ET.SubElement(bndbox2, 'xmin')
        xmin2.text = str(face[i][0])
        ymin2 = ET.SubElement(bndbox2, 'ymin')
        ymin2.text = str(face[i][1])
        xmax2 = ET.SubElement(bndbox2, 'xmax')
        xmax2.text = str(face[i][2])
        ymax2 = ET.SubElement(bndbox2, 'ymax')
        ymax2.text = str(face[i][3])

        filen, junk = nem.split('.')
        Tree.write('images/' + filen + '.xml')

    else:
        if os.path.exists('images/'+filen+'.jpg'):
            print('deleting: '+filen+'.jpg')
            os.remove('images/'+filen+'.jpg')