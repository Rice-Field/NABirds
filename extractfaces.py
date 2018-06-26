import matplotlib.pyplot as plt
from PIL import Image
from PIL import ImageOps
import numpy as np
import scipy as sp
import os
import cv2

Parts = np.loadtxt('parts/part_locs.txt', dtype=int, usecols = (1,2,3,4))
BB = np.loadtxt('bounding_boxes.txt', dtype=int, usecols = (1,2,3,4))
# 48562 total images
ID = np.genfromtxt('images.txt',dtype='str')
dim = np.loadtxt('sizes.txt', dtype=int, usecols = (1,2))

face = np.zeros([48562, 10], dtype=int)
faceBox = np.zeros([48562, 4], dtype=int)

j = 0
temp = 0
for i in range(len(Parts)):
	print('face point: %d' % i)
	# if parts arent visible, mark with -1
	# bill
	if Parts[i][0] == 0:
		if Parts[i][3] == 0:
			face[j][0] = -1
			face[j][1] = -1
		else:
			face[j][0] = Parts[i][1]
			face[j][1] = Parts[i][2]

	# crown
	if Parts[i][0] == 1:
		if Parts[i][3] == 0:
			face[j][2] = -1
			face[j][3] = -1
		else:
			face[j][2] = Parts[i][1]
			face[j][3] = Parts[i][2]

	# nape
	if Parts[i][0] == 2:
		if Parts[i][3] == 0:
			face[j][4] = -1
			face[j][5] = -1
		else:
			face[j][4] = Parts[i][1]
			face[j][5] = Parts[i][2]

	# left eye
	if Parts[i][0] == 3:
		if Parts[i][3] == 0:
			face[j][6] = -1
			face[j][7] = -1
		else:
			face[j][6] = Parts[i][1]
			face[j][7] = Parts[i][2]

	# right eye
	if Parts[i][0] == 4:
		if Parts[i][3] == 0:
			face[j][8] = -1
			face[j][9] = -1
			j += 1
		else:
			face[j][8] = Parts[i][1]
			face[j][9] = Parts[i][2]
			j += 1

		# check if right and left eye misslabeled
		if face[j-1][8] > face[j-1][6] and face[j-1][6] != -1:
			temp = face[j-1][8]
			face[j-1][8] = face[j-1][6]
			face[j-1][6] = temp


# from 5 points create face BBs
for i in range(len(face)):
	print('face box, image: %d' % (i+1))
	# main options:
	# bill nape crown, will have sub options
	# bill nape or crown and BB
	# both eyes, BB down to bill or nape

	# upright check might not be necessary
	upright = 0
	# determine if bird is upright or sideways with BB height and width
	if BB[i][3] > BB[i][2]:
		upright = 1

	if face[i][0] < 0 and face[i][4] < 0:
		faceBox[i][:] = -999
		continue

	# Both eyes and crown
	if face[i][6] > -1 and face[i][8] > -1 and face[i][2] > -1 and face[i][4] < 0:
		# print('both eyes')
		# bill is above eyes
		if face[i][1] < face[i][7] and face[i][1] < face[i][9]:
			# print('bill above eyes')
			# bill is even above crown
			if face[i][1] < face[i][3]:
				# print('bill above crown')
				faceBox[i][0] = face[i][8] - abs((face[i][9] - face[i][1])/2)
				faceBox[i][2] = face[i][6] + abs((face[i][9] - face[i][1])/2)
				faceBox[i][1] = face[i][3] - 10
				# determine which eye is furthest below
				if face[i][7] > face[i][9]:
					faceBox[i][3] = face[i][7] + abs((face[i][7] - face[i][1])/2)
				else:
					faceBox[i][3] = face[i][9] + abs((face[i][9] - face[i][1])/2)

				continue

			else:
				# print('bill below crown')
				faceBox[i][0] = face[i][8] - (face[i][9] - face[i][3])
				faceBox[i][2] = face[i][6] + (face[i][7] - face[i][3])
				faceBox[i][1] = face[i][3] - 10
				# determine which eye is furthest below
				if face[i][7] > face[i][9]:
					faceBox[i][3] = face[i][7] + abs((face[i][7] - face[i][3])/2)
				else:
					faceBox[i][3] = face[i][9] + abs((face[i][9] - face[i][3])/2)

				continue

		# bill above 1 eye and crown, turned head, currently image 33439 special case
		if (face[i][1] < face[i][7] or face[i][1] < face[i][9]) and face[i][1] < face[i][3]:
			# print('special case')
			faceBox[i][0] = face[i][2] - 20
			faceBox[i][1] = face[i][7] - 10
			faceBox[i][2] = face[i][1] + 10
			faceBox[i][3] = face[i][9] + 20
			continue

		# bill is below eyes
		# print('bill below eyes')
		faceBox[i][0] = face[i][8] - (face[i][1] - face[i][3])/2
		faceBox[i][2] = face[i][6] + (face[i][1] - face[i][3])/2
		faceBox[i][1] = face[i][3] - 10
		faceBox[i][3] = face[i][1] + 20

		continue

	# bill crown nape
	if face[i][0] > -1 and face[i][2] > -1 and face[i][4] > -1:
		# print('bill nape crown')

		if face[i][0] < face[i][4]:
			faceBox[i][0] = face[i][0] - 10
			faceBox[i][2] = face[i][4] + 10

		else:
			faceBox[i][0] = face[i][4] - 10
			faceBox[i][2] = face[i][0] + 10

		# upside down bird face
		if face[i][3] > face[i][5] and face[i][1] < face[i][3]:
			faceBox[i][1] = face[i][5] - 10
			faceBox[i][3] = face[i][3] + 20
			if face[i][6] != -1:
				if face[i][6] > face[i][0] and face[i][6] > face[i][4]:
					faceBox[i][2] = face[i][6] + abs((face[i][3] - face[i][7])/2)
				if face[i][6] < face[i][0] and face[i][6] < face[i][4]:
					faceBox[i][0] = face[i][6] - abs((face[i][3] - face[i][7])/2)

			if face[i][8] != -1:
				if face[i][8] > face[i][0] and face[i][8] > face[i][4]:
					faceBox[i][2] = face[i][8] + abs((face[i][3] - face[i][9])/2)
				if face[i][8] < face[i][0] and face[i][8] < face[i][4]:
					faceBox[i][0] = face[i][8] - abs((face[i][3] - face[i][9])/2)

			if face[i][2] < face[i][1] and face[i][2] < face[i][4]:
				faceBox[i][0] = face[i][2] - 20

			continue

		if face[i][1] < face[i][5]:
			faceBox[i][3] = face[i][5] + 20

		else:
			faceBox[i][3] = face[i][1] + 20

		if face[i][1] < face[i][3]:
			faceBox[i][1] = face[i][1] - 10

		else:
			faceBox[i][1] = face[i][3] - 10

		# bird has turned neck
		if face[i][2] < face[i][4] and face[i][2] < face[i][0]:
			faceBox[i][0] = face[i][2] - 20
		if face[i][2] > face[i][4] and face[i][2] > face[i][0]:
			faceBox[i][2] = face[i][2] + 20

		if face[i][6] != -1:
			if face[i][6] > face[i][0] and face[i][6] > face[i][2] and face[i][6] > face[i][4]:
				faceBox[i][2] = face[i][6] + abs((face[i][7] - face[i][3]))
			if face[i][6] < face[i][0] and face[i][6] < face[i][4] and face[i][6] < face[i][2]:
					faceBox[i][0] = face[i][6] - abs((face[i][3] - face[i][7])/2)

			if face[i][7] > face[i][1] and face[i][7] > face[i][3] and face[i][7] > face[i][5]:
				faceBox[i][3] = face[i][7] + abs((face[i][7] - face[i][3]))

		if face[i][8] != -1:
			if face[i][8] > face[i][0] and face[i][8] > face[i][4] and face[i][8] > face[i][2]:
					faceBox[i][2] = face[i][8] + abs((face[i][3] - face[i][9])/2)
			if face[i][8] < face[i][0] and face[i][8] < face[i][2] and face[i][8] < face[i][4]:
					faceBox[i][0] = face[i][8] - abs((face[i][3] - face[i][9])/2)

			if face[i][9] > face[i][1] and face[i][9] > face[i][3] and face[i][9] > face[i][5]:
				faceBox[i][3] = face[i][9] + abs((face[i][9] - face[i][3]))

		continue

	# bill nape
	if face[i][0] > -1 and face[i][4] > -1:
		# print('bill nape')

		if face[i][0] < face[i][4]:
			faceBox[i][0] = face[i][0] - 10
			faceBox[i][2] = face[i][4] + 10

		else:
			faceBox[i][0] = face[i][4] - 10
			faceBox[i][2] = face[i][0] + 10

		if face[i][1] < face[i][5]:
			faceBox[i][1] = face[i][1] - 10
			faceBox[i][3] = face[i][5] + 20

		else:
			faceBox[i][1] = face[i][5] - 10
			faceBox[i][3] = face[i][1] + 20

		if face[i][6] != -1:
			if face[i][6] > face[i][0] and face[i][6] > face[i][4]:
				faceBox[i][2] = face[i][6] + abs((face[i][7] - face[i][5])/2)
			if face[i][7] < face[i][1] and face[i][7] < face[i][5]:
				faceBox[i][1] = face[i][7] - abs((face[i][5] - face[i][7])/2)

		if face[i][8] != -1:
			if face[i][8] < face[i][0] and face[i][8] < face[i][4]:
				faceBox[i][0] = face[i][8] - abs((face[i][9] - face[i][5])/2)
			if face[i][9] < face[i][1] and face[i][9] < face[i][5]:
					faceBox[i][1] = face[i][9] - abs((face[i][5] - face[i][9])/2)

		continue

	# bill crown
	if face[i][0] > -1 and face[i][2] > -1:
		# print('bill crown')
		if face[i][0] < face[i][2]:
			faceBox[i][0] = face[i][0] - 10
			faceBox[i][2] = face[i][2] + 10

		else:
			faceBox[i][0] = face[i][2] - 10
			faceBox[i][2] = face[i][0] + 10

		if face[i][1] < face[i][3]:
			faceBox[i][1] = face[i][1] - 10
			faceBox[i][3] = face[i][3] + 20

		else:
			faceBox[i][1] = face[i][3] - 10
			faceBox[i][3] = face[i][1] + 20

		# if eye is present determine if it is out of crown/bill box
		if face[i][6] != -1:
			if face[i][6] > face[i][0] and face[i][6] > face[i][2]:
				faceBox[i][2] = face[i][6] + abs((face[i][7] - face[i][3]))

			if face[i][7] > face[i][1] and face[i][7] > face[i][3]:
				faceBox[i][3] = face[i][7] + abs((face[i][7] - face[i][3]))

		if face[i][8] != -1:
			if face[i][8] < face[i][0] and face[i][8] < face[i][2]:
				faceBox[i][0] = face[i][8] - abs((face[i][9] - face[i][3]))

			if face[i][9] > face[i][1] and face[i][9] > face[i][3]:
				faceBox[i][3] = face[i][9] + abs((face[i][9] - face[i][3]))

		continue

	# not a good face to use
	faceBox[i][:] = -999

# fix any birds on border that caused negative coordinates
# besides -999 which is bad face marker
for i in range(len(faceBox)):
	if faceBox[i][0] < 0 and faceBox[i][0] != -999:
		faceBox[i][0] = 0
	if faceBox[i][1] < 0 and faceBox[i][1] != -999:
		faceBox[i][1] = 0
	if faceBox[i][2] < 0 and faceBox[i][2] != -999:
		faceBox[i][2] = 0
	if faceBox[i][3] < 0 and faceBox[i][3] != -999:
		faceBox[i][3] = 0

	if faceBox[i][2] > dim[i][0]-1:
		faceBox[i][2] = dim[i][0]-1
	if faceBox[i][3] > dim[i][1]-1:
		faceBox[i][3] = dim[i][1]-1

	# either bad data or bad calc
	if faceBox[i][2] <= faceBox[i][0] and faceBox[i][0] != -999:
		print(str(i+1))
	if faceBox[i][3] <= faceBox[i][1] and faceBox[i][0] != -999:
		print(str(i+1))

np.savetxt('bird_faces.txt', faceBox, fmt='%d')
