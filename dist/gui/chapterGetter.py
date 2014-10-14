import sys
import requests as req
from bs4 import BeautifulSoup
import urlparse
import os

arguments = sys.argv

chapterLinks = []
chapterNumber = []
thisManga = {}



if len(arguments)==3 and sys.argv[0]=='chapterGetter.py':
	mangaName = sys.argv[2]
	mangaLink = sys.argv[1]
	html = req.get(mangaLink)
	soup = BeautifulSoup(html.text)
	chapters = soup.find(id="listing")
	chapters = chapters.find_all('a')
		
	#/temp/[mangaName]/

	path = os.path.dirname(os.path.abspath(__file__))+'/temp/'+mangaName

	if os.path.exists(path):
		chaptersFile = open(path+'/chapters.txt','w')
	else:
	
		os.makedirs(path)
		chaptersFile = open(path+'/chapters.txt','w')

	for link in chapters:
		jointLink = urlparse.urljoin(mangaLink,link.get('href')).encode('utf-8')
		name = link.text.encode('utf-8')
		thisManga[name] = jointLink
	chaptersFile.write(str(thisManga))

	chaptersFile.close()
	quit()
else:
	print "exiting"
	quit()


