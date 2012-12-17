#!/usr/bin/env python

import urllib
import urllib2
import urllib2 as urllib
import re
import sys
import urlparse
import random
from BeautifulSoup import BeautifulSoup
#email
import smtplib
from email import Encoders
from email.MIMEBase import MIMEBase
from email.MIMEImage import MIMEImage
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.Utils import formatdate

from PIL import Image
import StringIO
import resource







# --------------------------------------------------------------------------------------------------------------------------------------------------------------- #     
def getBaseDomain(url):
	"""Gets the base domain of the given url """
	return urlparse.urlparse(url).netloc

# --------------------------------------------------------------------------------------------------------------------------------------------------------------- #     
def getSubDomain(url):
	"""Gets the base domain of the given url """
	url = urlparse.urlparse(url)
	subdomain = url.hostname.split('.')[1]
	return subdomain

# --------------------------------------------------------------------------------------------------------------------------------------------------------------- #     
def removeNonSubUrlLinks(urlList):
	"""Remove all non-baseurl links from the list """
	newList = []
	for i in urlList:
		checkBaseUrl = getSubDomain(i)	
		if(checkBaseUrl == getSubDomain(baseUrl)):				
			newList.append(i)		
	return newList	

# --------------------------------------------------------------------------------------------------------------------------------------------------------------- #     
def removeNonBaseUrlLinks(urlList):
	"""Remove all non-baseurl links from the list """
	newList = []
	for i in urlList:
		checkBaseUrl = getBaseDomain(i)	
		if(checkBaseUrl == getBaseDomain(baseUrl)):				
			newList.append(i)		
	return newList	

# --------------------------------------------------------------------------------------------------------------------------------------------------------------- #     
def getAllImages(url):
	"""This gets only visible clickable links """		
	contents = urllib.urlopen(url).read()		
	soup = BeautifulSoup(contents)
	getBody = soup.findAll('img')
	#convert to string
	cvtToString = str(getBody)	

	links = re.findall(r'src=[\'"]?([^\'" >]+)', cvtToString)				
	
	return links

# --------------------------------------------------------------------------------------------------------------------------------------------------------------- #     
def getVisibleLinks(url):
	"""This gets only visible clickable links """		
	contents = urllib.urlopen(url).read()		
	soup = BeautifulSoup(contents)
	getBody = soup.findAll('a')
	#convert to string
	cvtToString = str(getBody)		
	links = re.findall(r'href=[\'"]?([^\'" >]+)', cvtToString)				
	regex = re.compile('\.jpg$|\.gif$|\.png$|\.pdf$|\.zip$', re.IGNORECASE)
	finalList = filter(lambda url: not regex.search(url), links)
	
	return finalList

# --------------------------------------------------------------------------------------------------------------------------------------------------------------- #     
def getAllUniqueLinks(baseUrl):
	"""Returns a unique list of urls """
	getBodyLinks = getVisibleLinks(baseUrl) 
	#remove all pound sign elements
	subList = removeFromList(getBodyLinks, '#')	
	#remove all non base url links
	#mainList = removeNonBaseUrlLinks(subList)
	mainList = subList
	#remove all duplicates
	finalList = list(set(mainList))		
	#Strip out similar duplicates by removing all / from urls that need it
	masterList = set(map(lambda url: url.rstrip('/'), finalList))
	listOfLinks = list(masterList)
	return listOfLinks

# --------------------------------------------------------------------------------------------------------------------------------------------------------------- #     
def getAllUniqueImgLinks(baseUrl):
	"""Returns a unique list of urls """
	getBodyLinks = getAllImages(baseUrl) 
	#remove all pound sign elements
	subList = removeFromList(getBodyLinks, '#')	
	#remove all non base url links
	#mainList = removeNonSubUrlLinks(subList)
	mainList = subList
	#remove all duplicates
	finalList = list(set(mainList))		
	#Strip out similar duplicates by removing all / from urls that need it
	masterList = set(map(lambda url: url.rstrip('/'), finalList))
	listOfLinks = list(masterList)
	return listOfLinks

# --------------------------------------------------------------------------------------------------------------------------------------------------------------- #     
def removeFromList(list, item):
	"""Remove a give value from a list """
	answer = []
	for i in list:
		if i!=item:
			answer.append(i)
	return answer

# --------------------------------------------------------------------------------------------------------------------------------------------------------------- #     
def sendImageEmail(me, you, subject, message, image):
	# Create message container - the correct MIME type is multipart/alternative.
	msg = MIMEMultipart('alternative')
	msg['Subject'] = subject
	msg['From'] = me
	msg['To'] = you

	# Create the body of the message (a plain-text and an HTML version).
	text = message
	html = "<html><head></head><body>"
	html += "<table border='0'>"
	for img in image:
		html += "<tr><td>"
		html += "<img src='"+str(img)+"' alt='Your image' />"
		html += "</tr><t/d>"
	html += "</table>"
	html += "</body></html>"

	# Record the MIME types of both parts - text/plain and text/html.
	part1 = MIMEText(text, 'plain')
	part2 = MIMEText(html, 'html')
	msg.attach(part1)
	msg.attach(part2)

	# Send the message via local SMTP server.
	s = smtplib.SMTP('localhost')
	s.sendmail(me, you, msg.as_string())
	s.quit()



if __name__ == '__main__':

	
	count = 0
	#stop_point = 10
	#minimim_height = 200
	imageEmailList = []
	finalList = set()
	subject = 'TEst'

	try:		
		baseUrl  = sys.argv[1]
		stop_point = sys.argv[2]
		minimim_height = sys.argv[3]
	except:
		baseUrl = 'http://www.zumiez.com'
		minimim_height = 200
		stop_point = 10
		print 'Using default baseUrl: ' + baseUrl
		print 'Using default stop_point: ' + str(stop_point)
		print 'Using default minimim height: ' + str(minimim_height)

	
	linksList = getAllUniqueLinks(baseUrl)


	for lk in linksList:


		
		#print lk
		#print stop_point
		try:
			imageList = getAllUniqueImgLinks(lk)


			totalImageLinks = len(imageList)
			ranId= random.randrange(0, totalImageLinks, 1)

			try:
				fd = urllib.urlopen(imageList[ranId])
				im = Image.open(StringIO.StringIO(fd.read())) 
				width = im.size[0]
				height = im.size[1]

				if(height > minimim_height):
				
					if(imageList[ranId] not in imageEmailList):
						#print str(count) +' link: '+ lk + ' image: ' + imageList[ranId] + ' '
						
						print '#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#'
						print str(count) + ') link: [' + lk + '] '
						print 'grabbing image: [' + imageList[ranId] + '] '
						print 'height: [' + str(height) + '] width: [' + str(width) + ']'
						print ''



						imageEmailList.append(imageList[ranId])



					if(count == stop_point):
						break

					count = count + 1
				else:
					continue

			except:
				continue
				print 'could not find url, passing....'
		except:
			continue
			print 'could not find url passing....'


	#print imageEmailList
	memory_usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
	print "Script memory usage: " + str(memory_usage)
	print "Total images sent: " + str(len(imageEmailList))
	print "Sending email"
	sendImageEmail('jasona@zumiez.com', 'jasona@zumiez.com', subject, 'testtest', imageEmailList)

