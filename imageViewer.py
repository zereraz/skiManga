from Tkinter import *
from PIL import Image,ImageTk
import sys
import os
import glob

imageList = []
imageWidthList = []
imageHeightList = []
arguments = sys.argv

#http://stackoverflow.com/questions/3085696/adding-a-scrollbar-to-a-grid-of-widgets-in-tkinter

        


path = os.path.dirname(os.path.abspath(__file__))+'/temp/Downloads/'
def imageFinder(folderName, mangaName):
	global path
	global imageList
	path += mangaName+'/'
	path += folderName+'/'
	imageList = glob.glob(path+'*.gif')


def onMouseWheel(event):
	global canvas
	canvas.yview_scroll(event.delta, "units")

counter = 0
def nextImage():
	global imageContainers
	global counter
	global canvas
	canvas.delete("all")
	canvas.yview_moveto(0)
	counter = (counter + 1)%len(imageContainers)
	canvas.create_image(imageWidthList[counter],300,image=imageContainers[counter])
	canvas.img = imageContainers[counter]

def prevImage():
	global imageContainers
	global counter
	global canvas
	global imageWidthList
	canvas.delete("all")
	canvas.delete(imageContainers[counter])
	counter = (counter - 1)%len(imageContainers)
	canvas.create_image(imageWidthList[counter],300,image=imageContainers[counter])
	canvas.img = imageContainers[counter]

def imageUpdater():
	global imageList
	global imageWidthList
	global imageHeightList
	for idx,image in enumerate(imageList):
		myImage = Image.open(image)
		imageWidthList.append(myImage.size[0])
		imageHeightList.append(myImage.size[1])
		myImage = ImageTk.PhotoImage(myImage)
		imageContainers.append(myImage)

if len(arguments) == 3:

	folderName = arguments[1] #chapterNumber
	mangaName = arguments[2]	
	root = Tk()
	canvas = Canvas(root,borderwidth=0,background="#ffffff")
	vsb = Scrollbar(root,orient="vertical",command=canvas.yview)
	canvas.bind_all("<MouseWheel>",onMouseWheel)
	canvas.configure(yscrollcommand=vsb.set)
	vsb.pack(side="right",fill="y")
	canvas.pack(side="left",fill="both",expand=True)
	imageFinder(folderName, mangaName)
	imageContainers = []
	buttonFrame = Frame(root)
	buttonFrame.pack(side=TOP)	
	next = Button(buttonFrame, text="Next", command=nextImage)
	prev = Button(buttonFrame, text="Prev", command=prevImage)
	refresh = Button(buttonFrame, text="Refresh", command=imageUpdater)
	imageUpdater()
	if len(imageContainers)!=0:
		#imageLabel.config(image=imageContainers[counter])
		#imageLabel.grid(row=2,column=1)
		canvas.create_image(imageWidthList[counter],0,image=imageContainers[counter],anchor="c")
		refresh.grid(row=0,column=1)
		next.grid(row=1,column=2)
		prev.grid(row=1,column=0)
	w,h = root.winfo_screenwidth(), root.winfo_screenheight()
	#root.overrideredirect(1)
	root.geometry("%dx%d+0+0"%(w,h))
	root.focus_set()
	
	root.lift()
	root.mainloop()
		

else:	
	quit()
