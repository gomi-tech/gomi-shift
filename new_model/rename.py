import os

img_dir = 'lait'
if not os.path.isdir(img_dir):
	os.mkdir(img_dir)

milk_folders = [folder for folder in os.listdir('.') if 'milk' in folder]

# print(milk_folders)

n = 0
for folder in milk_folders:
	for img_file in os.scandir(folder):
		os.rename(img_file.path, os.path.join(img_dir, '{:08}.jpg'.format(n)))
		n = n + 1