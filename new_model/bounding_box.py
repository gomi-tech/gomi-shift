import os 
import matplotlib.pyplot as plt
import cv2
from matplotlib.widgets import RectangleSelector
from xml_gen import write_xml

# global constants
img = None
top_left_list = []
bot_right_list = []
obj_list = []

# folder locations
img_folder = 'C:\\Users\\ericl\\Documents\\Gomi\\darkflow\\images\\test'
savedir = 'C:\\Users\\ericl\\Documents\\Gomi\\darkflow\\images\\test_annotations'
obj = 'milk'

def line_select(click, release):
	# print(click.xdata, click.ydata)
	global top_left_list
	global bot_right_list
	top_left_list.append((int(click.xdata), int(click.ydata)))
	bot_right_list.append((int(release.xdata), int(release.ydata)))
	obj_list.append(obj)
	print(top_left_list, bot_right_list)
	print('Press q to save coordinates, press c to  clear coordinates')

def toggle_selector(event):
	toggle_selector.RS.set_active(True)

def on_key_press(event):
	global img
	global top_left_list
	global bot_right_list
	global obj_list
	
	# saves drawns boxes
	if event.key == 'q':
		print('Saved Coordinates {}, {}'.
			format(top_left_list, bot_right_list))
		write_xml(img_folder, img, obj_list, top_left_list, 
			bot_right_list, savedir)
		img = None
		top_left_list = []
		bot_right_list = []
		obj_list = []
		plt.close()

	# resets drawn boxes
	if event.key == 'c':
		img = None
		top_left_list = []
		bot_right_list = []
		obj_list = []
		print('Reset boxes: top_left {}, bot_right {}'.
			format(top_left_list, bot_right_list))

if __name__ == '__main__':
	for n, img_file in enumerate(os.scandir(img_folder)):
		img = img_file
		fig, ax = plt.subplots(1)
		image = cv2.imread(img_file.path)
		image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
		# print("n is {}".format(n))
		# print("img_file is {}".format(img_file))
		# ax.set_title(img_file)
		ax.imshow(image)

		toggle_selector.RS = RectangleSelector(
			ax, 
			line_select, 
			drawtype='box', 
			useblit=True,
			button=[1], 
			minspanx=5, 
			minspany=5, 
			spancoords='pixels',
			interactive=True
		)
		bbox = plt.connect('key_press_event', toggle_selector)
		key = plt.connect('key_press_event', on_key_press)
		plt.show()
		# plt.close(fig)