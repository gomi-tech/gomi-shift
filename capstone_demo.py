import cv2
from darkflow.net.build import TFNet
import numpy as np
from collections import defaultdict

class Vision():
    def __init__(self):
        self.options = {
                        'model': 'cfg/yolov2-tiny-voc-5c.cfg',
                        'load': 25675,
                        'threshold': 0.25,
                       }
        self.tfnet = TFNet(self.options)
        self.colors = [185, 255, 255]
        self.elements = 10
        self.threshold = 0.35

        # initialize dictionary defaultdict allows arrays in value of dictionary
        self.inventory = defaultdict(list)
        self.master_inventory = defaultdict(list)

        # initialize camera
        self.cap = cv2.VideoCapture(1)

    def gen_box(self, colors, results, frame):
        # if results is empty then add zeros to the dictionary valuse of the labels
        # inside of the dictionary
        self.check_empty(results)

        items = []
        # only executes this look if results is not empty
        for color, result in zip(colors, results):
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

        # add zeros to items that are not detected
        self.add_zeros(items)

    # checks to see if list is larger than 10, if it is then remove the first element
    # and then add the new element to the end
    def check_label(self, text, items):
        label = text.split(': ')[0]
        confidence = text.split(': ')[1]
        # check to see if label is in dictionary and adds it only if the threshold
        # is greater than 0.50, if label not in dictionary then length will be 0 
        #  to begin with
        if ((label not in self.inventory) and (float(confidence) > self.threshold)):
            self.inventory[label].append(confidence)
        else:
            # label is in dictionary check length of label value in dictionary
            # if it is greater than 10 then snip the size from the front
            if len(self.inventory[label]) == self.elements:
                self.inventory[label].pop(0)
            # checks to see confidence of label is greater than the threshold
            # and if the values in the label in dictionary are less than the 
            # specified element size
            if ((float(confidence) > self.threshold)):
                self.inventory[label].append(confidence)

    # check to see if list is empty
    def check_empty(self, results):
        if not results:
            for key in self.inventory:
                # check length of inventory if its larger than threshold then pop
                if (len(self.inventory[key]) == self.elements):
                    self.inventory[key].pop(0)
                else:
                    # print('adding zeros')
                    self.inventory[key].append('0')

    # add zeros to items if not detected 
    def add_zeros(self, items):
        for entry in self.inventory:
            # check length of inventory if its larger than threshold then pop
            if (len(self.inventory[entry]) == self.elements):
                self.inventory[entry].pop(0)
            else:
                # print('adding zeros')
                if entry not in items:
                    self.inventory[entry].append('0')

    # calculates average of values in dictionary
    def average(self):
        average_arr = []
        key_arr = []
        for key in self.inventory:
            key_arr.append(key)
            if len(self.inventory[key]) != 0:
                total = sum([float(items) for items in self.inventory[key]])
                average = total/len(self.inventory[key])
                # if average > self.threshold:
                average_arr.append(average)
                if key not in self.master_inventory:
                    self.master_inventory[key].append(average)
                # print(key)
        return average_arr, key_arr

    # adding to master inventoryS
    # def add_to_master(self, avg, key):
    #     if avg != 0:
    #         for number in range(len(avg)):
    #             # adds to master
    #             if (avg[number] > self.threshold):
    #                 if key[number] not in self.master_inventory:
    #                     print('Adding from master: {}'.format(number))
    #                     self.master_inventory[key[number]].append(avg[number])
    #             # removes from master 
    #             if (avg[number] < self.threshold):
    #                 if key[number] in self.master_inventory:
    #                     print('Removing from master: {}'.format(number))
    #                     del self.master_inventory[key[number]]
    #                     del key[number]
    #                     del avg[number]
                        # number = number - 1

    # updates the frame and bounding boxes
    def update(self):
        ret, frame = self.cap.read()
        results = self.tfnet.return_predict(frame)
        if ret:
            self.gen_box(self.colors, results, frame)
            avg, key = self.average()
            for val in range(len(avg)):
                if avg[val] < self.threshold and any(self.master_inventory):
                    del self.inventory[key[val]]
                    del self.master_inventory[key[val]]
                    del key[val]
            # self.add_to_master(avg, key)
            # print('Average is: {}'.format(avg))
            # print('Inventory is: {}'.format(self.inventory))
            # print('Average is: {}\nItems in key: {}'.format(avg, key))
            print('Inventory: {}'.format(self.inventory))
            print('Master Inventory: {}'.format(self.master_inventory))
            # print('Master Inventory is: {}'.format(self.master_inventory))
            # print('This is the avg {} and key : {}'.format(avg,key))
            # if avg != 0:
            #   for number in range(len(avg)):
            #       # print(number)
            #       # print('number {}'.format(number))
            #       # print('key {}'.format(key))
            #       if (avg[number] > self.threshold):
            #           self.master_inventory[key[number]].append(avg[number])
                        # print(self.master_inventory)
                # for number in avg:
                #   print('number {}'.format(number))
                #   print('key {}'.format(key))
                #   if (number > self.threshold):
             #          self.master_inventory[key].append(number)
             #          print(self.master_inventory)

    # # stops the frame capture
    def stop(self):
        self.cap.release
        cv2.destoryAllWindows()

if __name__=="__main__":
    test = Vision()
    while True:
        test.update()
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    test.stop()