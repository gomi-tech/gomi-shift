import final_capstone_demo as OR
import displaywebcam_2 as UI
import tkinter

# Setup window
window = tkinter.Tk()
# window.resizable(width=False, height=False)
data = UI.App(window, "GOMI S.H.I.F.T.")

# Setup computer vision
test = OR.Vision()

print("done")
while(1):
	ret, frame = test.update()
	data.update_list(test.master_inventory)
	data.update(ret, frame)
	window.update_idletasks()
	window.update()