import cv2
import os
import numpy as np

# directory = 'C:\\Users\\ericl\\Documents\\Gomi\\darkflow\\images\
# \\resized-images-on-camera'
# file_name = []
directory = 'C:\\Users\\ericl\\Desktop\\resized-images-on-BLU_ONE_2'

for n, img_file in enumerate(os.scandir(directory)):
	image = cv2.imread(img_file.path)
	resize = cv2.resize(image, None, fx=0.5, fy=0.5, 
		interpolation=cv2.INTER_CUBIC)
	cv2.imwrite(img_file.path, resize)
	# file_name.append(img_file)
	# print(img_file)
	# print(file_name)
	# print("n is {}".format(n))
	# print("img_file is {}".format(img_file))
# print(img_file)