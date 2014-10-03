#!/usr/bin/python
import os
import Tkinter
from PIL import Image,ImageTk
def gui():
	root = Tkinter.Tk()	
	title = "mangaReader"
	root.title(title)
	message = "Images"
	downloadMessage = "Download Manga"
	download = Tkinter.Button(root, text = downloadMessage,command = callDownloader)
	path = os.path.dirname(os.path.abspath('gui.py'));
	path = path+"/images/theo.jpg"
	myImage = Image.open(path)
	currentImage = ImageTk.PhotoImage(myImage)
	topLabel = Tkinter.Label(root, text = message, fg = "red")
	imageLabel = Tkinter.Label(root) 
	imageLabel.config(image = currentImage)
	topLabel.pack()
	download.pack()
	imageLabel.pack()
	root.mainloop()
def main():
	gui()
def callDownloader():
	os.system("python downloader.py mangareader")



if __name__ == '__main__':
	main()
