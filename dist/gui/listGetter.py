#!/usr/bin/env python

import requests as req
from bs4 import BeautifulSoup
import urlparse
import os
baseUrl = 'http://mangareader.net'


listGetHtml = req.get('http://www.mangareader.net/alphabetical')

soup = BeautifulSoup(listGetHtml.text)

mangaDivContainers = soup.find_all('div', class_ = "series_alpha")

mangaLinks = []
mangaNames = []
mangas = {}

for div in mangaDivContainers:
	mangaLinks.append(div.find_all('a'))

linkFile = open('linkFile.txt','w')

for linkArr in mangaLinks:
	for link in linkArr:
		if(link.get('href') != '#top'):
			name = link.text.encode('utf-8')
			link = link.get('href')	
			jointUrl = urlparse.urljoin(baseUrl,link).encode('utf-8')
			mangas[name] = jointUrl 
			
linkFile.write(str(mangas))
			

linkFile.close()
#os.system('python gui.py')
quit()
