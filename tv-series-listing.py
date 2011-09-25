#Python 2.7
#Author n!ghtf0x
#email anirvan.mandal@gmail.com
#Script for retreving Tv show information from TVrage.com
#uses tvrage apy for python ver 0.3.0
#visit http://static-point.blogspot.com/2011/09/python-script-airing-time-and-date-for.html  for links to pytz and tvrage api

from tvrage import quickinfo # --> python-tvrage-api 0.3.0 
import string
import pytz # pytz --> for time zone conversion
import datetime
from time import mktime
from math import trunc
import time
import tvrage

#time zones -- to convert the given time of episode airing to the desired timezone for example EST to IST
us = pytz.timezone('America/New_York')
india = pytz.timezone('Asia/Calcutta')

#SeriesList -- The list of tv show names for which we want to collect the information #infoList -- List to which series information is appended
SeriesList = ['supernatural 2005','one tree hill 2003','the big bang theory 2007','strike back 2010','breaking bad 2008', 'the vampire diaries 2009', 'how i met your mother 2005','castle 2009','modern family 2009','nikita 2010','the mentalist 2008','fringe 2008','the good wife 2009', 'gossip girl 2007','dexter 2006','house 2004','chuck 2007']		
infoList = []

# Note -- Add TV show names in the format "tv_show_name(small letters) year of premier"

		
def timeFix(list): # function for conversion of airing time
		time = str(list['Airtime'])
		try:
				nextDate = (list['Next Episode'])
				nextDateWithTime = time + ' ' + nextDate[2]
				nextDateStrip = datetime.datetime.strptime(nextDateWithTime,'%A at %I:%M %p %b/%d/%Y')
				timeWithZoneus = us.localize(nextDateStrip)
				timeWithZonein = timeWithZoneus.astimezone(india)
				timeStamp = mktime(nextDateStrip.timetuple())
				nextDateWithTime = timeWithZonein.strftime('%A at %I:%M %p %b/%d/%Y')
				(list['Next Episode'])[2] = nextDateWithTime
				
		except KeyError:
				#print " Next episode information does not exist !" 
				list['Next Episode'] = ['N/A','N/A','N/A'] #since information of the next episode is not available
				timeStamp = '0'
		
		
		prevDate = (list['Latest Episode'])
		
		
		
		
		prevDateWithTime = time + ' ' + prevDate[2]
		prevDateStrip = datetime.datetime.strptime(prevDateWithTime,'%A at %I:%M %p %b/%d/%Y')
		timeWithZoneus = us.localize(prevDateStrip)
		timeWithZonein = timeWithZoneus.astimezone(india)
		prevDateWithTime = timeWithZonein.strftime('%A at %I:%M %p %b/%d/%Y')
		(list['Latest Episode'])[2] = prevDateWithTime
		infoList.append([list['Show Name'],(list['Next Episode'])[0],(list['Next Episode'])[1],(list['Next Episode'])[2],timeStamp]) #all the desired information -- checkout pytvrage api for other information
		return list
		
	
try:
		i = 0
		while i <= 16:
				try:
						#print i --used for debugging
						seriesInfo = quickinfo.fetch(SeriesList[i])
						series_time_fixed = timeFix(seriesInfo)# Print series_time_fixed[] for having a look at various information returned by tvrage
						
						i = i+1
				except tvrage.util.TvrageError: # If server does not reply 
						print "Retrying " 
						
						
						
				
		
		# creating the key for sorting according to time of release		
		def stamp(t):
				return t[4]
		sortedInfoList = sorted(infoList,key=stamp)
		
		#Printing the data in a desired format
		print 'Title'.ljust(25,' ')  +'Next Episode'.ljust(18,' ')  + 'Episode name'.ljust(30,' ') + 'Airing Time (IST)'.ljust(30,' ') 
		for x in sortedInfoList:
				print x[0].ljust(25,' ')  +x[1].ljust(18,' ')  + x[2].ljust(30,' ') + x[3].ljust(30,' ')
except AttributeError:# When no internet connectivity is found --> restart script
		print "\n\n\tCheck Your Internet Connectivity !\n"
