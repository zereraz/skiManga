import os
from PIL import Image
import sys
import requests as req
from bs4 import BeautifulSoup
import PIL.Image
from StringIO import StringIO
import urlparse
from Tkinter import *
from ttk import *
import threading

#global
arguments = sys.argv
maxPageNo = 0
imagePageLinks = []
imageLinks = []
baseUrl = 'http://www.mangareader.net'


def chapterInfo(chapterLink, mangaName, progressBar):
	global imagePageLinks
	global baseUrl
	global maxPageNo
	html = req.get(chapterLink)
	soup = BeautifulSoup(html.text)
	select = soup.find(id="pageMenu")
	options = select.find_all('option')
	for option in options:
		imagePageLinks.append(urlparse.urljoin(baseUrl,option.get('value').encode('utf-8')))
	maxPageNo = len(imagePageLinks)
	imagesDownloadLinks(progressBar,mangaName)

def imagesDownloadLinks(progressBar, mangaName):
	global imagePageLinks
	mangaName = '_'.join(mangaName.split(' '))
	path = os.path.dirname(os.path.abspath(__file__))+'/temp/Downloads/'+mangaName
	for idx,link in enumerate(imagePageLinks):
		html = req.get(link)
		soup = BeautifulSoup(html.text)
		imageDiv = soup.find(id="imgholder")
		imageLink = imageDiv.find_all('img')[0]
		imageLink = imageLink.get('src')
		imageLinks.append(imageLink)
		progressBar["value"]+=1		
	
		try:
			imagePage = req.get(imageLink)			
			image = PIL.Image.open(StringIO(imagePage.content))			

		except req.exceptions.RequestException as e:
			print e

		if not os.path.exists(path):
				os.makedirs(path)
		try:
			image.save(path+'/'+str(idx)+'.gif',"GIF")
		except Exception as e:
			print "Error "+str(e)	
		
		



def start(progressBar):
	progressBar["value"] = 0
	progressBar["maximum"] = maxPageNo


if len(arguments) == 3:	
	chapterLink = arguments[1]
	mangaName = arguments[2]
	root = Tk()
	progressBar = Progressbar(root,orient="horizontal",mode="determinate",length=500)	
	progressBar.pack()
	t = threading.Thread(target=chapterInfo,args = (chapterLink, mangaName,progressBar))
	t.daemon = True
	t.start()
	root.mainloop()
	quit()
	
else:
	print arguments
	quit()
