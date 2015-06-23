from subprocess import Popen
import sys
import urllib2
import time

# Poll Hub interface to determine free/busy status of resources
def freeCheck():
	free=0
	wait=0
	try:
		response=urllib2.urlopen('http://localhost:4200/grid/console')
		time.sleep(2)
		html=response.read()
		# Check to see if any browsers are available
		free = html.count("platform=")
		print 'free:'+str(free)
		# Check to see if any scripts are queued
		wait = html.count("waiting")
		print 'wait:'+str(wait)
		#exit
	except urllib2.URLError:
		count = 0
	except urllib2.HTTPError:
		count = 0
	pass

	# if any scripts queued, stop and do nothing further
	if wait > 0:
		count=0
	# if slots are free, proceed
	elif free > 0:
		count=free
	# otherwise, do nothing further
	else:
		count=0
	print 'return count of:'+str(count)
	return count

# If resources available (first condition) add more requests
#   - rename whatever test you want to run to the 'sdtest.py' value
# Otherwise, exit and wait a while
#if 'type=WebDriver' in html:
freeCount=0
freeCount=freeCheck()
#print 'freeCount before loop:'+str(freeCount)
while freeCount>2:
	#print 'I have entered the loop'
	ex=Popen('python test.py 4500&',shell=True,close_fds=True)
	exOut=ex.communicate()
	print(exOut)
	try:
		time.sleep(1)
		try:
			freeCount=freeCheck()        
		except:
			freeCount=0
			exit
		print('fc:'+str(freeCount))

	except:
		#print 'something failed, so leaving'
		freeCount=0
		time.sleep(30)
		exit




		
