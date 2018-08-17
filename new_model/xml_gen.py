import os
import cv2
from lxml import etree
import xml.etree.cElementTree as ET

def write_xml(folder, img, objects, top_left, bot_right, savedir):
	if not os.path.isdir(savedir):
		os.mkdir(savedir)

	image = cv2.imread(img.path)
	height, width, depth = image.shape

	annotation = ET.Element('annotation')
	ET.SubElement(annotation, 'folder').text = folder
	ET.SubElement(annotation, 'filename').text = img.name
	size = ET.SubElement(annotation, 'size')
	ET.SubElement(size, 'width').text = str(width)
	ET.SubElement(size, 'height').text = str(height)
	ET.SubElement(size, 'depth').text = str(depth)
	ET.SubElement(annotation, 'segmented').text = '0'

	for obj, topl, botr in zip(objects, top_left, bot_right):
		ob = ET.SubElement(annotation, 'object')
		ET.SubElement(ob, 'name').text = obj
		ET.SubElement(ob, 'pose').text = 'Unspecified'
		ET.SubElement(ob, 'truncated').text = '0'
		ET.SubElement(ob, 'difficult').text = '0'
		bbox = ET.SubElement(ob, 'bndbox')
		ET.SubElement(bbox, 'xmin').text = str(topl[0])
		ET.SubElement(bbox, 'ymin').text = str(topl[1])
		ET.SubElement(bbox, 'xmax').text = str(botr[0])
		ET.SubElement(bbox, 'ymax').text = str(botr[1])

	xml_str = ET.tostring(annotation)
	root = etree.fromstring(xml_str)
	xml_str = etree.tostring(root, pretty_print=True)

	save_path = os.path.join(savedir, img.name.replace('jpg', 'xml'))
	with open(save_path, 'wb') as temp_xml:
		temp_xml.write(xml_str)

# for testing
# if __name__ == '__main__':
	# folder = '/home/ericly/Documents/train-pi/images/test'
	# img = [im for im in os.scandir(folder) if '00000000' in im.name][0]
	# objects = ['milk']
	# top_left = [(10, 10)]
	# bot_right = [(100, 100)]
	# savedir = '/home/ericly/Documents/train-pi/images/test_annotations'
	# write_xml(folder, img, objects, top_left, bot_right, savedir)