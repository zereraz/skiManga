#!/bin/usr/env pyhton

from Tkinter import *
from PIL import Image,ImageTk
import requests as req
from bs4 import BeautifulSoup
from StringIO import StringIO
import os
import tkMessageBox
import subprocess
import shutil


#global

chapterButtonNames = ["Download Chapter","Download all Chapters","Read Chapter(not save)"]
chapterButtonWidgets = []
currentChapterLink = ""
currentMangaName = ""


if not os.path.isfile('linkFile.txt'):
	print "Loading Manga's"
	p = subprocess.Popen('python listGetter.py',shell=True)
	p.wait()


root = Tk()
root.state('zoomed')
root.title = "SkiManga"
root.minsize(300,300)
path = os.path.dirname(os.path.abspath(__file__))+'/'
mangaDict = {}
chapterDict = {"None":"None"}
status = Label(root, text = "", bd = 1, relief = SUNKEN, anchor = W)
status.pack(side = BOTTOM, fill = X)
path = os.path.dirname(os.path.abspath(__file__))

def updateMangaList():
	os.system("python listGetter.py")


def ask_quit():
	status.config(text="Quiting")
	if tkMessageBox.askyesno("Quit", "Do you want to Quit?"):
		if tkMessageBox.askyesno("Delete Temporary Files", "Do you want to remove the temporary files?"):	
			path = os.path.dirname(os.path.abspath(__file__))+'/temp/'
			if os.path.exists(path):
				shutil.rmtree(path)	
		root.destroy()


def onSelect(*args):
	status.config(text="selecting manga")
	key = selectedItem.get()
	mangaLink = mangaDict[key]
	imageName = '_'.join(key.split(' '))	
	if not os.path.isfile('temp/'+imageName+'.gif'):
		status.config(text="Fetching information")
		downloadImage(mangaLink)
	else:
		imageUpdate(mangaLink)	
	global currentMangaName
	currentMangaName = imageName
	getChapterList(mangaLink,imageName)


def getChapterList(mangaLink, mangaName):
	global chapterDict
	command = "python chapterGetter.py "+mangaLink+' '+mangaName
	p = subprocess.Popen(command,shell=True)
	p.wait()

	with open(path+'/temp/'+mangaName+'/chapters.txt','r') as f:
		status.config(text="getting chapter list for manga")
		chapterDict = eval(f.read())
		
	chapterSelected.set(chapterDict.keys()[0])
	updateOptionMenu()

def updateOptionMenu():
	global chapterDict
	chapterOptionMenu['menu'].delete(0,'end')	
	for chapters in chapterDict:
		chapterOptionMenu['menu'].add_command(label=chapters,command=lambda chapters = chapters:chapterSelected.set(chapters))


def onChapterSelected(*args):
	global chapterDict
	chapterName =  chapterSelected.get()
	chapterLink = chapterDict[chapterName]
	global currentChapterLink
	currentChapterLink = chapterLink


def addButtons():
	global chapterButtonNames
	global chapterButtonWidgets
	if(len(chapterButtonWidgets) == 0):
		for idx,buttonName in enumerate(chapterButtonNames):
			chapterButtonWidgets.append(Button(buttonFrames, text=buttonName))
			chapterButtonWidgets[idx].pack()
		addCommands()
	else:
		del chapterButtonWidgets[:]
		addButtons()
	

def addCommands():
	global chapterButtonWidgets
	chapterButtonWidgets[0].configure(command = downloadChapter)
	chapterButtonWidgets[1].configure(command = downloadAllChapters)
	chapterButtonWidgets[2].configure(command = readThisChapter)

mangaImageLinks = []

def downloadChapter():
	global chapterButtonWidgets
	global currentChapterLink
	global currentMangaName
	command = 'python chapterDownloader.py '+currentChapterLink+' '+currentMangaName

	p = subprocess.Popen(command,shell=True)



def downloadAllChapters():			
	print "B"

def readThisChapter():
	print "A"

def downloadImage(mangaLink):
	status.config(text="Getting information")

	try:
		html = req.get(mangaLink)
	except req.exceptions.RequestException as e:
		print e
		status.config(text="Check internet connection")
		return
	soup = BeautifulSoup(html.text)
	imageUrl = soup.find(id="mangaimg").img.get('src')
	try:
		imagePage = req.get(imageUrl)
		image = Image.open(StringIO(imagePage.content))
	except req.exceptions.RequestException as e:
		print e
		status.config(text="Check internet connection")
		return
	path = os.path.dirname(os.path.abspath(__file__))+'/temp/'
	if not os.path.exists(path):
		os.makedirs(path)
	try:
		imageName = '_'.join(selectedItem.get().split(' '))
		image.save(path+imageName+'.gif',"GIF")
		status.config(text="success")
		imageUpdate(mangaLink)
	except Exception as e:
		print "Error "+str(e)+" "+selectedItem.get()
		status.config(text="error")
		return	

def imageUpdate(mangaLink):
	imageName = '_'.join(selectedItem.get().split(' '))+'.gif'
	path = os.path.dirname(os.path.abspath(__file__))+'/temp/'
	myImage = ImageTk.PhotoImage(Image.open(path+imageName))
	imageLabel.config(image = myImage)
	imageLabel.image = myImage
	status.config(text="Getting Summary")
	getSummary(mangaLink)

def getSummary(mangaLink):
	
	try:
		html = req.get(mangaLink)
	except req.exceptions.RequestException as e:
		print e
		status.config(text="error")
		return
	soup = BeautifulSoup(html.text)
	div = soup.find(id="readmangasum")	
	summary =  div.p.contents

	if len(summary)>0:
		summary = summary[0].encode('utf-8')
	updateSummary(summary)

def updateSummary(summary):
	global summaryVar
	if len(summary)>0:
		summaryVar.set(summary)
	else:
		summaryVar.set("Summary not available")

with open("linkFile.txt") as f:
	status.config(text="Reading Temporary files")
	mangaDict = eval(f.read())

selectedItem = StringVar()
chapterSelected = StringVar()

chapterSelected.set(chapterDict.keys()[0])

selectedItem.set(mangaDict.keys()[0])
optionFrame = Frame(root, bd=1, relief=SUNKEN, padx=2, pady=2, height=3)
option = OptionMenu(optionFrame, selectedItem,*mangaDict.keys())


buttonFrames = Frame(root,bd=1,relief=SUNKEN, padx=2, pady=2)
buttonFrames.pack(side=TOP)
updateMangaButton = Button(buttonFrames,text="update manga list",command=updateMangaList)
updateMangaButton.pack(side=TOP)

infoFrame = Frame(root, bd=1, relief=SUNKEN, padx=2, pady=2)
infoFrame.pack(side=LEFT)

imageFrame = Frame(infoFrame, bd=1, relief=SUNKEN, padx=2, pady=2)
imageFrame.pack(side=TOP)


option.pack(side=LEFT)
optionFrame.pack(side=RIGHT)


#Chapter Information
chapterFrame = Frame(root,bd=1,relief=SUNKEN,padx=2,pady=2)
chapterFrame.pack(side=BOTTOM)
chapterLabel = Label(chapterFrame, text="Chapter List")
chapterLabel.pack()
chapterOptionMenu = OptionMenu(chapterFrame, chapterSelected, *chapterDict) 
chapterOptionMenu.pack()

#Summary information
summaryFrame = Frame(infoFrame, bd=1, relief=SUNKEN, padx=2, pady=2)
summaryFrame.pack(side=BOTTOM)
summaryVar = StringVar()
summaryLabel = Label(summaryFrame, textvariable=summaryVar, wraplength=300)
summaryVar.set("summary")
summaryLabel.pack()

#Manga Image
imageLabel = Label(imageFrame, text="manga image")
imageLabel.pack()
selectedItem.trace("w", onSelect)
chapterSelected.trace("w", onChapterSelected)
root.protocol('WM_DELETE_WINDOW', ask_quit)

addButtons()


root.lift()
root.mainloop()


