#! /usr/bin/env python


import requests
from bs4 import BeautifulSoup
from StringIO import StringIO
from PIL import Image
import os
import urlparse

#global variable path
path = "allDownloadedImages/"

#check if the url is absolute or not
#relative urls need to be joint to form absolute url

def isAbsolute(url):
	return bool(urlparse.urlparse(url).netloc)

def downloader():
	print "create a new folder to store downloaded images? yes or no?"
	option = raw_input()
	if option.lower() == 'yes':
		pathChanger()
	print "Enter url"
	url = raw_input()
	if url=='':
		downloader()
	else:
		html = requests.get(url)
		soup = BeautifulSoup(html.text)
		images = soup.find_all('img')
		numbering = 0
		for i in images:
			imageName = i.get('alt') or str(numbering)
			imageUrl = i.get('src')
			#if url is relative, make it absolute
			if not isAbsolute(imageUrl):
				imageUrl = urlparse.urljoin(url,imageUrl)
			print imageUrl

			try:
				imagePage = requests.get(imageUrl)
				image = Image.open(StringIO(imagePage.content))
			except requests.exceptions.RequestException as e:
				print e
				quit()
			if not os.path.exists(path):
				os.makedirs(path)	
			try:
				imageUrl = imageUrl.split('/')
				imageUrl = imageUrl[len(imageUrl)-1]
				fileName = str(imageName)[0:5]+'_'+str(imageUrl)[0:]
				image.save(path+fileName)
				print fileName +" Downloaded !"
			except Exception as e:
				print "Error "+str(e)+" "+fileName
				continue

def pathChanger():
	print "Enter new path"
	global path 
	path = raw_input()
	if path[len(path)-1] == '/':
		return
	else:
		path = path+ '/'	

def main():
	downloader()
if __name__ == '__main__':
	main()
