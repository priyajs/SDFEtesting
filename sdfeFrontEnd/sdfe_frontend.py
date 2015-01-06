from selenium import webdriver
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import datetime
import csv
import random
import sys
import urllib2
#import mechanize

'''
#--- Get Interactive Input ----------------------------------
#--- Number of iterations to execute ------------------------
#numLoops = int(sys.argv[1])
#------------------------------------------------
#--- Browser definition --------------------------------------
#browser = sys.argv[2]

#--- SeGrid Hub designation ----------------------------------
#hub = sys.argv[3]
#instID = sys.argv[4]

#--- End of Interactive Input --------------------------------
'''
duration = int(sys.argv[1])

#--- Read List of PIIs ---------------------------------------
PII=[]

try:
 csvRd = csv.reader(open('/home/ubuntu/sdfePIIwhitelist.csv','rb'))
 print('Successfully opened the datafile')
except:
 csvRd = csv.reader(open('C:\scripts\whitelist_piis.csv','rb'))
 print('Successfully opened the datafile')
 #sys.exit(1)
for everyItem in csvRd:
        PII.append(everyItem) 
	
#------------------------------------------------
#       Function to gracefully exit the browser
#               after incrementing loop variables
#------------------------------------------------
def egress():
        try:
                driver.quit()
        #except WindowsError:
        #        print ("****WindowsError - pass? ****")
        #        pass
        except urllib2.URLError:
                print ("----URLError - pass? ----")
                pass


#------------------------------------------------------
# Function to send error details for tracking
#------------------------------------------------------
def errorReport(hName,titlN,msg):
 sendBack='http://cert-pa.elsevier.com/perfTest?perfTest.error.cpc=SD&perfTest.error.cpc.host='+hName+'&perfTest.error.cpc.host.page='+titl+'&perfTest.error.cpc.host.page.msg='+msg
 try:
  url2Send = urllib2.urlopen(sendBack)        
  #print('error url sent')
 except:
  #print('error url NOT sent')
  pass


#------------------------------------------------------
# Function to send error details for tracking
#------------------------------------------------------
def newBrowser(base):
 sendBack='http://cert-pa.elsevier.com/perfTest?perfTest.cpc=SD&perfTest.cpc.'+base+'.newBrowser=1&perfTest.cpc.'+base+'.id='+instID
 try:
  url2Send = urllib2.urlopen(sendBack)        
  #print('error url sent')
 except:
  #print('error url NOT sent')
  pass


#-------------------------------------------------------
#      Function to execute a request or page interaction
#      handles associated error conditions
#      Makes call to collect page timing
#--------------------------------------------------------
def getPage(resource):
 try:
  #driver.get("http://"+baseURL)
  resource
  #print driver.title
  if 'Unable to process' in driver.title:
	print 'Error - Unable to process, wait 60 seconds'
	errorReport(base,titl,'Unable to Process')
	time.sleep(10)
	exit
  elif 'ScienceDirect Error' in driver.title:
   	dt = datetime.datetime.now()
   	dTm = str(dt.strftime("%Y/%m/%d %H:%M:%S%Z"))
   	print 'SD-00x Error'+dTm
   	errorReport(base,titl,'SD-00x')
   	time.sleep(1)
   	exit
  elif 'Error' in driver.title:
   	print 'Error, wait 60 seconds'
   	time.sleep(10)
   	exit
  else:
   	if 'SD Content Delivery' in titl:
   	#metricsCollect(titl,Pii)
    		time.sleep(2)
    	pass
#  else:
#   	#metricsCollect(titl,'NA')
#    	pass
#      
#  time.sleep(.25)
   
  """
   try:
    wp=0
    wpEnt = driver.execute_script("return window.performance.getEntries().length")
    while(wp != wpEnt):
     time.sleep(.25)
     wpEnt= wp
     wp = driver.execute_script("return window.performance.getEntries().length")
     #print('wpEnt:'+str(wpEnt)+' wp:'+str(wp))
   except:
   pass
  """
 except urllib2.URLError:
  print 'URLError'
  errorReport(base,titl,'URLError')
  pass
 except:
     #####################################################
     #seeing lots of failures here due to special characters in title... need to look into it
     #it was due to print driver.title with special characters
     #####################################################
  print (titl+' fail')
  errorReport(base,titl,'Other')
  pass

#-----------------------------------------------------------------------
#       Function to capture various page timing metrics
#               and output to screen for log tailing and troubleshooting
#------------------------------------------------------------------------

#def metricsCollect(dtitl,PII,sections):
def metricsCollect(dtitl,ID):
        try:
                navS = driver.execute_script("return performance.timing.navigationStart")
                #print(navS)
                respS = driver.execute_script("return performance.timing.responseStart")
                respE = driver.execute_script("return performance.timing.responseEnd")
                dom = driver.execute_script("return performance.timing.domInteractive")
                loadE = driver.execute_script("return performance.timing.loadEventEnd")
                domC = str(driver.execute_script("return document.getElementsByTagName('*').length"))
                if loadE > navS:
                        pgLoad = str(int(loadE-navS))
                        domI = str(int(dom-navS))
                        cont = str(int(respE-navS))
                        ttfb = str(int(respS-navS))
                        #print('\nperf details found\n')
                else:
                        pgLoad = 'NA'
                        domI='NA'
                        cont='NA'
                        ttfb = 'NA'
                        #print('perf details NOT found')
 
                # Datetime for Timestamp
                dt = datetime.datetime.now()
                dTm = str(dt.strftime("%Y/%m/%d %H:%M:%S%Z"))
                
                if 'SD Content Delivery' in dtitl:
                #       if sections > 0:
                #               print(browser+'\t'+dTm+'\t'+pgLoad+'\t'+domI+'\t'+cont+'\t'+ttfb+'\t'+domC+'\t'+PII+'\t'+sections)
                #       else:
                        print(browser+'\t'+dTm+'\t'+pgLoad+'\t'+domI+'\t'+cont+'\t'+ttfb+'\t'+domC+'\t'+ID)
                else:
                        print(browser+'\t'+dTm+'\t'+pgLoad+'\t'+domI+'\t'+cont+'\t'+ttfb+'\t'+domC+'\t'+dtitl)
                
        except:
                if 'Pii' in globals():
                        print('Unable to print perfTiming details, PII:'+Pii)
                else:
                        print('Unable to print perfTiming details')
                try:
                        driver.quit()
                #except WindowsError:
                #       print ("******WindowsError - pass? ****")
                #       pass
                except urllib2.URLError:
                                print ("------URLError - pass? ----")
                                pass
# ---------------------
# End metricsCollect()
# ---------------------

#=============================================================
#-------------------------------------------------------------
#       Script Begins Here
# opens a browser , reads random pii from a csv file, authentication and actual article as seperate items.
#using time instead of numloops.
#-------------------------------------------------------------
#=============================================================

#--- Define static Article Value for looping

#idx=0
#numLoops=3
loop = 1

#duration = 300
teststarttime = time.time()
print 'teststarttime: '+str(teststarttime)
timetoendtest = int(teststarttime + duration)
print 'timetoendtest: '+str(timetoendtest)
#-------------------------------------------------
#       Define baseURL for following transactions
#-------------------------------------------------
baseURL='www.test.sdfe.sciencedirect.com'
base='SDFE'
username='sdfe-engineers'
password='Target947Tirpitz'

while int(time.time()) < timetoendtest:
#while numLoops > loop:
	print'loop:'+str(loop)
	try:
		driver=webdriver.Chrome()
		time.sleep(.25)
		print 'setting browser'

		try:
			newBrowser(base)
		except:
			pass
		##-this section needed only if authentication has to be seperated from actual article rendering##
		##- else comment this section and uncomment	#theURL='http://'+username+':'+password+'@'+baseURL+'/science/article/pii/'+Pii in the block below##
		#theURL='http://'+username+':'+password+'@'+baseURL+'/science'
		#driver.get(theURL)
		#print 'opened page/authentication: '+theURL
		##-this section needed only if authentication has to be seperated from actual article rendering##							
		browserLoop = 4
		while (browserLoop > 0):   	
			print'browserloop:'+str(browserLoop)
			titl = 'Article Page'
			idx = random.randrange(0,4345,1)
			print str(idx)
			Pii = str(PII[idx]).strip('[\']')
			print Pii 
			   
			try:
				theURL='http://'+username+':'+password+'@'+baseURL+'/science/article/pii/'+Pii
				#theURL='http://'+baseURL+'/science/article/pii/'+Pii
				getPage(driver.get(theURL))
				print 'opened page: '+theURL
				#print driver.title
			except urllib2.URLError:
				time.sleep(.25) 
				pass
     					
			browserLoop = browserLoop - 1
			#print'browserloop:'+str(browserLoop)
			
		loop = loop + 1            
		egress()
		print"exit browser"
        	        	
	except:
		loop = loop +1
		egress()
		print datetime.datetime.now()
		print 'failure'
		errorReport(base, titl, 'Start Browser Fail')
		time.sleep(5)
		#egress()
		pass
else:
	print 'test ended @'+str(time.time())
	
	
	
