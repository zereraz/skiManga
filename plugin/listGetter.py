#!/usr/bin/env python

import requests as req
from bs4 import BeautifulSoup
import urlparse
baseUrl = 'http://mangareader.net'

listGetHtml = req.get('http://www.mangareader.net/alphabetical')

soup = BeautifulSoup(listGetHtml.text)

mangaDivContainers = soup.find_all('div', class_ = "series_alpha")

mangaLinks = []

for div in mangaDivContainers:
	mangaLinks.append(div.find_all('a'))

linkFile = open('linkFile.txt','w')

for linkArr in mangaLinks:
	for link in linkArr:
		link = link.get('href')
		if(link != '#top'):
			jointUrl = urlparse.urljoin(baseUrl,link)
			linkFile.write(jointUrl+'\n')

linkFile.close()
