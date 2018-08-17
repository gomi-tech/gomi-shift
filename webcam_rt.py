import cv2
from darkflow.net.build import TFNet
import numpy as np
from collections import defaultdict

# options = {
# 	'model': 'cfg/yolov2-tiny-voc-5c.cfg',
# 	'load': 25675,
# 	'threshold': 0.40,
# }
# tfnet = TFNet(options)
# colors = [185, 255, 255]

# # dictionary use inventory.append(confidence)
# inventory = {}

# # initialize camera
# cap = cv2.VideoCapture(1)

# lists of items to calulate moving average
# milk, yogurt, peanut, lemon, tomato = ([] for i in range(5))

class Vision():
	def __init__(self):
		self.options = {
						'model': 'cfg/yolov2-tiny-voc-5c.cfg',
						'load': 25675,
						'threshold': 0.35,
					   }
		self.tfnet = TFNet(self.options)
		self.colors = [185, 255, 255]
		self.elements = 10
		self.threshold = 0.5
		# initialize dictionary defaultdict allows arrays in value of dictionary
		self.inventory = defaultdict(list)
		self.master_inventory = defaultdict(list)
		# initialize camera
		self.cap = cv2.VideoCapture(1)

	def gen_box(self, colors, results, frame):
		# if results is empty then add zeros to the dictionary valuse of the labels
		# inside of the dictionary
		# print('detecting these items: {}'.format(results))
		if not results:
			# print('hello')
			for key in self.inventory:
				# print('in key loop')
				# check length of inventory if its larger than threshold then pop
				if (len(self.inventory[key]) == self.elements):
					self.inventory[key].pop(0)
				# print('the items in inventory are')
				# print('The len is: {}'.format(len(self.inventory)))
				else:
					# print('adding zeros')
					self.inventory[key].append('0')
		# print(self.inventory)
		items = []
		# only executes this look if results is not empty
		# print('print result(s): {}'.format(results))
		for color, result in zip(colors, results):
			# print('print result: {}'.format(result))
			# print('this is the results {}'.format(result))
			topleft = (result['topleft']['x'], result['topleft']['y'])
			btmright = (result['bottomright']['x'], result['bottomright']['y'])
			label = result['label']
			confidence = result['confidence']
			text = '{}: {:.2f}'.format(label, confidence)
			items.append(label)
			self.check_label(text, items)
			frame = cv2.rectangle(frame, topleft, btmright, color, 5)
			frame = cv2.putText(
				frame, text, topleft, cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,0), 2)
		cv2.imshow('frame', frame)
		# print('Items in gen_box: {}'.format(items))

		for entry in self.inventory:
			# print('in key loop')
			print('Entry = {}'.format(entry))
			# check length of inventory if its larger than threshold then pop
			if (len(self.inventory[entry]) == self.elements):
				self.inventory[entry].pop(0)
			# print('the items in inventory are')
			# print('The len is: {}'.format(len(self.inventory)))
			else:
				# print('adding zeros')
				if entry not in items:
					# print('Items: {} and key:{}'.format(items, key))
					print('Entry = {} \nItems = {}'.format(entry, items))
					self.inventory[entry].append('0')

		# print(self.inventory)
		# print('This is items: {}'.format(items))
	# if results are not in dictionary add them, otherwise add zeroes to the rest
	# def check_results(self, label, confidence):
	# 	for key in self.inventory.keys():
	# 		if key == label:
	# 			continue
	# 		else:
	# 			self.inventory[key].append(0)
				# print(self.inventory)
			# if label not in self.inventory:
			# 	self.inventory[label].append(confidence)
			# else:
			# 	self.inventory[key].append(0)

	# checks to see if list is larger than 10, if it is then remove the first element
	# and then add the new element to the end
	def check_label(self, text, items):
		# used to control number of frames
		# elements = 10
		label = text.split(': ')[0]
		confidence = text.split(': ')[1]
		# check to see if label is in dictionary and adds it only if the threshold
		# is greater than 0.50, if label not in dictionary then length will be 0 
		#  to begin with
		if ((label not in self.inventory) and (float(confidence) > self.threshold)):
			self.inventory[label].append(confidence)
			# print(self.inventory)
		else:
			# print('The labels are {}'.format(label))
			# label is in dictionary check length of label value in dictionary
			# if it is greater than 10 then snip the size from the front
			# print('The the length of inventory label are {}'.format(len(self.inventory[label])))
			if len(self.inventory[label]) == self.elements:
				self.inventory[label].pop(0)
				# print('popped an entry to make space')
			# checks to see confidence of label is greater than the threshold
			# and if the values in the label in dictionary are less than the 
			# specified element size
			if ((float(confidence) > self.threshold)):
				self.inventory[label].append(confidence)
				# print(self.inventory)
			# for entry in self.inventory:
			# 	# print('in key loop')
			# 	print('Entry = {}'.format(entry))
			# 	# check length of inventory if its larger than threshold then pop
			# 	if (len(self.inventory[entry]) == self.elements):
			# 		self.inventory[entry].pop(0)
			# 	# print('the items in inventory are')
			# 	# print('The len is: {}'.format(len(self.inventory)))
			# 	else:
			# 		# print('adding zeros')
			# 		if entry not in items:
			# 			# print('Items: {} and key:{}'.format(items, key))
			# 			print('Entry = {} \nItems = {}'.format(entry, items))
			# 			self.inventory[entry].append(0)
						# # do not add a zero
						# if (len(self.inventory[items]) == self.elements):
						# 	self.inventory[items].pop(0)
						# # print('These are the items: {}'.format(items))
						# # self.inventory[key].append('0')
						# else:
						# 	# print('adding zeros')
						# 	self.inventory[items].append('0')

		# print(self.inventory)
			# look at items in the dictionary that are not on the labels, add a zero
			# element to them
			# for key in self.inventory:
			# 	# adds a zero the label in the dictionary that is not in the current label
			# 	# and checks size of the array
			# 	if len(self.inventory[label])+1 == elements:
			# 		self.inventory[label].pop()
			# 		# print('popped an entry to make space')
			# 	if ((key != label) and (len(self.inventory[label]) < elements)):
			# 		self.inventory[key].append('0')
			# 		# print(self.inventory)
			# 	# else:
			# 		# make space by popping
			# print(self.inventory)
			# for value in self.inventory[label]:
			# 	number = float(value)
			# 	print(number)
			# if number > threshold:
			# 	print('This item > threshold {}'.format(self.inventory))

		# print('This is the text {}'.format(text))
		# self.check_results(label, confidence)
		# self.check_confidence(label, confidence)
		# check to see if label exists in dictionary if it doesn't then add it
		# self.check_length(label, confidence)
		# print('This is the check_label print: {}'.format(self.inventory[label]))
		# if len(self.inventory[label]) > threshold:
		# 	self.inventory[label].pop()
		# 	# self.inventory[label].append(confidence)
		# 	print('inside if {}'.format(self.inventory))
		# else:
		# if label not in self.inventory:
		# self.inventory[label].append(confidence)
		# print(self.inventory)
		# total = sum(self.inventory[label])
		# print(total)
		# self.check_confidence(label, confidence)
		# self.inventory[label].append(confidence)
		# print('otuside if {}'.format(self.inventory))
			# self.add_to_inv(label, confidence)
			# self.check_confidence(label, confidence)

	# # takes the average of the readings and makes sure the values is above 0.50
	# def check_confidence(self, label, confidence):
	# 	# total = sum([float(i) for i in self.inventory[label]])
	# 	# total = sum(self.inventory[label])
	# 	total = 0
	# 	for i in self.inventory[label]:
	# 		total = total + float(i)
	# 	# print(total)
	# 	# print(self.inventory)
	# 	# checks to see if new item is placed
	# 	if ((total/len(self.inventory)) > 0.50):
	# 		# append to database
	# 		self.inventory[label].append(confidence)
	# 		# print('inside check_confidence if {}'.format(self.inventory))

	# updates the frame and bounding boxes
	def update(self):
		ret, frame = self.cap.read()
		results = self.tfnet.return_predict(frame)
		if ret:
			self.gen_box(self.colors, results, frame)
			print(self.inventory)
	
	# stops the frame capture
	def stop(self):
		self.cap.release
		cv2.destoryAllWindows()

# generate box, and prediction (label and confidence)
# def gen_box(colors, results, frame):
# 	for color, result in zip(colors, results):
# 		# checks to see if results is empty
# 		topleft = (result['topleft']['x'], result['topleft']['y'])
# 		btmright = (result['bottomright']['x'], result['bottomright']['y'])
# 		label = result['label']
# 		confidence = result['confidence']
# 		text = '{}: {:.2f}'.format(label, confidence)
# 		check_label(text)
# 		frame = cv2.rectangle(frame, topleft, btmright, color, 5)
# 		frame = cv2.putText(
# 			frame, text, topleft, cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,0), 2)
# 	cv2.imshow('frame', frame)

# check to see what label it is found
# def check_label(text):
# 	# global flag
# 	# print('flag in check label {}'.format(flag))
# 	label = text.split(': ')[0]
# 	confidence = text.split(': ')[1]
# 	if label == "Milk Carton (2L)":
# 		# check to see if its new or old
# 		check_list(milk, confidence)
# 		check_confidence(milk, label, confidence)
# 		# print('{}: {}'.format('milk', milk))
# 	if label == "Yogurt (tub)":
# 		# check to see if its new or old
# 		check_list(yogurt, confidence)
# 		check_confidence(yogurt, label, confidence)
# 		# print('{}: {}'.format('yogurt', yogurt))
# 	if label == "Peanut Butter (tub)":
# 		# check to see if its new or old
# 		check_list(peanut, confidence)
# 		# print('{}: {}'.format('peanut', peanut))
# 	if label == "Lemon":
# 		# check to see if its new or old
# 		check_list(lemon, confidence)
# 		check_confidence(lemon, label, confidence)
# 		# print('{}: {}'.format('lemon', lemon))
# 	if label == "Tomato":
# 		# check to see if its new or old
# 		check_list(tomato, confidence)
# 		# print('{}: {}'.format('tomato', tomato))

# # checks to see if the list is larger than 10, if it is then pop out the first element
# def check_list(list, confidence):
# 	if len(list) > 10:
# 		list.pop(0)
# 		list.append(confidence)
# 	else:
# 		list.append(confidence)

# takes an average of the last 10 readings and sees if its > 0.50
# def check_confidence(list, label, confidence):
# 	global flag
# 	total = sum([float(i) for i in list])
# 	# checks to see if new item is placed
# 	if ((total/len(list)) > 0.50):
# 		# append to database, check to see if flag is 1, if flag is 1 skip
# 		# don't update flag until item is removed
# 		# if flag == 0:
# 			# append to database
# 			# print('Added: {}'.format(label))
# 		inventory[label].append(confidence)
# 		print(inventory)
		# set flag to not check if this item is added, flag is not working
		# flag = 1
	# print('flag: {}'.format(flag))
	# threshold of 10 for buffer, to check if we have zeros
	# if ((total/len(list)) < 0.10):
	# 	print('Removed: {}'.format(label))
	# 	flag = 0

# def run_webcam():
# 	while True:
# 		ret, frame = cap.read()
# 		results = tfnet.return_predict(frame)
# 		if ret:
# 			gen_box(colors, results, frame)
# 		if cv2.waitKey(1) & 0xFF == ord('q'):
# 			break
# 	cap.release
# 	cv2.destoryAllWindows()

if __name__=="__main__":
	test = Vision()
	while True:
		test.update()
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
	test.stop()