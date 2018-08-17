import xml.etree.ElementTree as ET
import os

# directory = 'C:\\Users\\ericl\\Documents\\Gomi\\darkflow\\images\
# \\resized-camera_annotations'
directory = 'C:\\Users\\ericl\\Documents\\Gomi\\darkflow\
\\new_images\\old-annotations\\new-lemons-annotations'

# def resize_image(arg, xml):
# 	for string in root.iter(arg):
# 		new_string = int(int(string.text)/2)
# 		string.text = str(new_string)
# 		tree.write(xml)

def rename_xml(arg, xml, name):
	for string in root.iter(arg):
		# new_string = int(int(string.text)/2)
		if name == 68:
			continue
		new_string = str(name)
		string.text = (new_string+'.xml')
		print(string.text)
		tree.write(xml)

for n, xml_file in enumerate(os.scandir(directory)):
	tree = ET.parse(xml_file.path)
	root = tree.getroot()
	print(n)
	rename_xml('filename', xml_file.path, n)


	# resize_image('width', xml_file.path)
	# resize_image('height', xml_file.path)
	# resize_image('xmin', xml_file.path)
	# resize_image('ymin', xml_file.path)
	# resize_image('xmax', xml_file.path)
	# resize_image('ymax', xml_file.path)

	# for width in root.iter('width'):
	# 	# print(width)
	# 	new_width = int(int(width.text)/2)
	# 	# print(new_width)
	# 	width.text = str(new_width)
	# 	tree.write(xml_file.path)

	# for height in root.iter('height'):
	# 	new_height = int(int(height.text)/2)
	# 	height.text = str(new_height)
	# 	tree.write(xml_file.path)

	# for xmin in root.iter('xmin'):
	# 	new_xmin = int(int(xmin.text)/2)
	# 	xmin.text = 

	# for size in root.findall('size'):
	# 	width = str(int(int(size.find('width').text)/2))
	# 	height = str(int(int(size.find('height').text)/2))
		# print(width, height)
		# tree.find('annotation/size/width').text = width
		# tree.find('annotation/size/height').text = height
		# tree.write(xml_file.path)

	# for obj in root.findall('object/bndbox'):
	# 	xmin = str(int(int(obj.find('xmin').text)/2))
	# 	ymin = str(int(int(obj.find('ymin').text)/2))
	# 	xmax = str(int(int(obj.find('xmax').text)/2))
	# 	ymax = str(int(int(obj.find('ymax').text)/2))
		# print(xmin,ymin,xmax,ymax)
		# tree.find('annotation/object/bndbox/xmin').text = xmin
		# tree.find('annotation/object/bndbox/ymin').text = ymin
		# tree.find('annotation/object/bndbox/xmax').text = xmax
		# tree.find('annotation/object/bndbox/ymax').text = ymax
		# tree.write(xml_file.path)

	# print(root[4][1].text)