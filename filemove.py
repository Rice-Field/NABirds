# move images out of folders
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
import scipy as sp
import os
import glob

for i in range(483, 1011):
	if i < 1000:

		if not os.path.exists('images/'+'{}'.format(i).zfill(4)+'/'):
			continue

		for filename in glob.glob('images/'+'{}'.format(i).zfill(4)+'/*.jpg'):
			print(filename)
			fuld, nem = filename.split("\\")
			os.rename(filename, ("images/"+nem))
	else:
		if not os.path.exists('images/'+'{}'.format(i)+'/'):
			print('lol')
			continue

		for filename in glob.glob('images/'+'{}'.format(i)+'/*.jpg'):
			print(filename)
			fuld, nem = filename.split("\\")
			os.rename(filename, ("images/"+nem))