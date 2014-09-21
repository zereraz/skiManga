#!/usr/bin/python

import Tkinter
from PIL import Image,ImageTk
def main():
	root = Tkinter.Tk()	
	title = "mangaReader"
	root.title(title)
	message = "Images"
	path = "/Users/balvindersingh/Documents/python/mangaReader/images/theo.jpg"
	myImage = Image.open(path)
	currentImage = ImageTk.PhotoImage(myImage)
	topLabel = Tkinter.Label(root, text = message, fg = "red")
	imageLabel = Tkinter.Label(root) 
	imageLabel.config(image = currentImage)
	topLabel.pack()
	imageLabel.pack()
	root.mainloop()		

if __name__ == '__main__':
	main()
