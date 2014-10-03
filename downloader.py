import requests
import sys

arguments = sys.argv

argumentNumber = len(arguments)


# download the chapter

def downloadChapter(mangaSite,mangaName,mangaName,chapterName):
	website = requests.get(mangaName+str('/')+mangaName+('/')+chapterName)

# get page and show it
 
def readPage(mangaSite,mangaName,chapterName,pageNumber):
	


if argumentNumber > 1:
	scriptName = arguments[0]
else:
	print "Script invoked without any arguments"
	quit()

if scriptName == 'downloader.py':
	
	if argumentNumber == 1:
		print "Only script name sent"
		quit()
	else:
		if argumentNumber == 2:
			print "Please Enter The Manga name and chapter"
			quit()
		else:
			if argumentNumber == 4:
				print "Downloading full chapter"
				mangaSite = arguments[1]
				mangaName = arguments[2]
				chapterNumber = arguments[3]
				downloadChapter(mangaSite,mangaName,chapterName)
			elif argumentNumber == 5:
				pageNumber = arguments[4]
				readPage(mangaSite,mangaName,chapterName,pageNumber)
			else:
				print "Argument number > 5"
				quit()
else:
	print "Wrong script, this is downloader.py"
	quit()

