import tkinter
import cv2
import PIL.Image, PIL.ImageTk
import time

class App:
    def __init__(self, window, window_title, video_source=0):
        self.window = window
        self.window.title(window_title)
        self.video_source = video_source

        # open video source (by default this will try to open the computer webcam)
        self.vid = MyVideoCapture(self.video_source)

        # Create a canvas that can fit the above video source size
        self.canvas = tkinter.Canvas(window, width = self.vid.width, height = self.vid.height)
        self.canvas.grid(row=2, column=0,rowspan=10,pady=50, padx=50)

        # # Button that lets the user take a snapshot
        # self.btn_snapshot=tkinter.Button(window, text="Take a Picture", width=50, command=self.snapshot)
        # self.btn_snapshot.grid(row=11)

        ######

        self.title1= tkinter.Label(window, text="My Fridge", bg="#13EE0C", fg="white", font=('comic sans','50'),width=28)
        self.title1.grid(row=0, columnspan=5, rowspan=2)



		#My List Title
        self.title2 = tkinter.Label(window, text="My Inventory", font="20")
        self.title2.grid(row=2, column=1, ipady=10,padx=0)


		#Delete Items
        # self.nameE = tkinter.Entry(window)
        # self.nameE.grid(row=3, column=1)

        #self.delButton = tkinter.Button(window, text="Enter", command=self.Delete) #when you click it, the command 'fssignup' will run. which is the def
        #self.delButton.grid(row=3, column=2, sticky="W")




		#Set up the list window for Items
        self.lb = tkinter.Listbox(window, height = 20, width=30, selectmode="MULTIPLE")
        self.lb.insert(tkinter.END, 'Nothing')
        self.lb.grid(row=4,column=1, padx=50)
        ######################


        # After it is called once, the update method will be automatically called every delay milliseconds
        #self.delay = 15
        #self.update()

        #self.window.mainloop()

    def update_list(self, dictionary):

        # Make a function to append the window based on the contents of Master Dictionary
        key = dictionary.keys()
        self.lb.delete(0,tkinter.END)
        for item in key:
             self.lb.insert(tkinter.END, item)
             self.lb.grid(row=4,column=1, padx=50)

    def snapshot(self, ret, frame):

        if ret:
            cv2.imwrite("frame-" + time.strftime("%d-%m-%Y_%H-%M-%S") + ".jpg", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

    def Delete(self):
        string=self.nameE.get()
        int_ans=int(string)
        self.lb.delete(int_ans)



    def update(self, ret, frame):
        # Get a frame from the video source
        #ret, frame = self.vid.get_frame()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image = self.photo, anchor = tkinter.NW)

        #self.window.after(self.delay, self.update)


class MyVideoCapture:
    def __init__(self, video_source=0):
        # Open the video source
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)

        # Get video source width and height
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                # Return a boolean success flag and the current frame converted to BGR
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return (ret, None)
        else:
            return (ret, None)

    # Release the video source when the object is destroyed
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()
