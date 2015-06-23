from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
#import datetime
import csv
import random
import sys
import urllib2
import socket

#from metricsCollect import metricsCollect

#------------------------------------------------------------
#--- Get Interactive Input for number of loops to execute ---
#numLoops = int(sys.argv[1])
timeToRun=int(sys.argv[1])
# timeToRun = 3800
endTime=int(time.time()+timeToRun)

env=sys.argv[2]

cpc='sdfe'

#--- Browser definition for Grid usage ----------
# browser = sys.argv[2]
browser = 'chrome'

#--- SeGrid Hub designation --------------------
# hub = sys.argv[3]
hub='localhost'


#statsDHost='ec2-54-80-6-76.compute-1.amazonaws.com'
statsDHost='statsd.elsst.com'
"""
  Define UDP connection to send data to statsD
"""
UDPSock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
## statsd host & port
addr=(statsDHost,8125)


#--- Read List of PIIs -----------------
PII=[]

if(int(time.time())%3==0):
    pdfFile='sdfePIIwhitelist1.1_1.csv'
if(int(time.time())%3==1):
    pdfFile='sdfePIIwhitelist1.1_2.csv'
if(int(time.time())%3==2): 
    pdfFile='sdfePIIwhitelist1.1_3.csv'


try:
  # csvRd = csv.reader(open('/home/ubuntu/PIIs_20k.csv','rb'))
    csvRd = csv.reader(open('/home/ubuntu/'+pdfFile,'rb'))
    piiCount = 490000
except:
    # csvRd = csv.reader(open('./sdfePIIwhitelist1.1_1.csv','rb'))
    csvRd = csv.reader(open('./'+pdfFile,'rb'))
    piiCount = 490000
for j in csvRd:
    PII.append(j)



#---------------------------------------
#       Function to gracefully exit the browser
#               after incrementing loop variables
#-----------
def egress():
    try:
        driver.quit()
    except urllib2.URLError:
        # print ("----URLError - pass? ----")
        pass


#------------------------------------------------------
# Gather Performance data to send
#------------------------------------------------------
def metricsCollect(dtitl,d):#,baseIn):
    # print('in metricsCollect')
    l=[]
    l.append(cpc+'.Selenium.'+env+'.'+titl+'.pass:1|c\n')
    metrics={'ttfb':'responseStart','html':'responseEnd','pgi':'domInteractive','pgl':'loadEventEnd','startRender':'domContentLoadedEventEnd'}
    try:
        navS = d.execute_script('return performance.timing.navigationStart')
        for i in metrics:
            compVal=int(d.execute_script('return performance.timing.'+metrics[i])-navS)
            if(compVal>0):
                l.append(cpc+'.Selenium.'+env+'.'+dtitl+'.'+str(i)+':'+str(compVal)+'|ms\n')

        try:
            prsT=[]
            prs=d.execute_script('return prs')
            try:
                prsT.append(prs['pcr'])
            except:
                pass
            try:
                prsT.append(prs['pcr_nav'])
            except:
                pass
            try:
                prsT.append(prs['abs_end'])
            except:
                pass
            pcrT=sorted(prsT)[len(prsT)-1]
        except:
            pcrT=0
        if pcrT > navS:
            l.append(cpc+'.Selenium.'+env+'.'+dtitl+'.pcr:'+str(int(pcrT-navS))+'|ms\n')
    except:
        pass

    # print('l is:')
    # print(l)
    # print 'join statsDdata'
    statsDdata=''.join(l)
    # print('here is statsDdata')
    # print(statsDdata)

    try:
    	# print('try to send UDP message')
    	# print 
        UDPSock.sendto(statsDdata,addr)
    
    except:
    	print('UDP send failed')
    	pass


#------------------------------------------------------
#       Function to execute a request or page interaction
#               handles associated error conditions
#               Makes call to collect page timing
#-------------
def getPage(resource):
    try:
        #driver.get("http://"+baseURL)
        resource
        if 'Unable to process' in driver.title:
            # print 'Error - Unable to process, wait 60 seconds'
            time.sleep(60)
            exit
        elif 'ScienceDirect Error' in driver.title:
            # print 'SD-00x Error'+dTm
            time.sleep(1)
            exit
        elif 'Error' in driver.title:
            # print 'Error, wait 60 seconds'
            time.sleep(10)
            exit
        else:
            time.sleep(.5)
        # print('trying metricsCollect')
        try:
            # print('try to append to stats')
            sdmExists = driver.execute_script("return typeof(SDM)")
            if 'object' in sdmExists:
            # if 'ScienceDirect' in driver.title:
                time.sleep(.25)
                metricsCollect(titl,driver)#,base)

        except:
            pass

    except urllib2.URLError:
        # print 'URLError'
        pass
    except:
        # print (titl+' fail')
        pass


#=============================================================
#-------------------------------------------------------------
#       Script Begins Here
#-------------------------------------------------------------
#=============================================================
#--- Define static Article Value for looping
idx=0
while endTime > time.time():
    """
    Define capabilities of remote webdriver
    		Specifically: assign browser type
    """
    try:
        # print('loading browser')
        # driver=webdriver.Remote("http://"+hub+":4200/wd/hub",desired_capabilities={"browserName": browser})
        # driver=webdriver.Chrome()

        options=webdriver.ChromeOptions()
        options.add_argument('--disable-logging')
        driver=webdriver.Remote("http://"+hub+":4200/wd/hub",desired_capabilities=options.to_capabilities())
        print('wait for it...')
        # print datetime.datetime.now()
        time.sleep(.25)

        driver.set_window_size(1100,800)

        # Initialize array for holding metrics to send to graphite
        # l = []


        #-------------------------------------------------
        #       Define baseURL for following transactions
        #-------------------------------------------------
        baseIDX=int(random.random()*100)

        if (baseIDX%2==0):
            baseURL = 'www.sciencedirect.com'
            base='currProd'
        if (baseIDX%2==1):
            baseURL = 'www-new.sciencedirect.com'
            base='newProd'

        baseURL = 'www.qa.sdfe.sciencedirect.com'
        base='sdfe.'+env


        #-------------------------------------------------
        #      Add looping structure to minimize browser churn
        #-------------------------------------------------
        browserLoop=1#2
        while(browserLoop > 0):
            #-------------------------------------------------
            #       View Article(s) with scrolling where possible
            #               View multiple articles in same session 33%
            #-------------------------------------------------
            artLoop = 5
            """
            if (login%3==0):
            artLoop=8
            else:
            artLoop=4
            """
            # print ('artLoop: '+str(artLoop))

            #Comment out for sequential evaluation of articles
            #idx = int(random.random()*499000)


            while artLoop > 0:
                #--- Define Random Value ---------------
                idx = int(random.random()*piiCount)
                idxPii=idx
                # print('articleIDX:'+str(idx))
                Pii=str(PII[idxPii]).strip('[\']')
                # print Pii
                # Pii='S0001731010004679'
                titl = 'Content_Delivery'
                #sStart = time.time()
                try:
                    # print('try to get: '+"http://"+baseURL+"/science/article/pii/"+Pii)
                    getPage(driver.get("http://"+baseURL+"/science/article/pii/"+Pii))
                    time.sleep(random.randrange(20,40,1)/10)
                    # print(driver.title)
                    try:
                        pdfLink=driver.find_element_by_link_text('Download full text in PDF')
                        # print('clicking PDF link')
                        pdfLink.click()
			time.sleep(3)
                        # driver.save_screenshot('afterPDF-'+Pii+'.png')
			# time.sleep(.25)

                        try:
			    
                            downCheck=driver.execute_script("return document.getElementById('download-checkbox').getBoundingClientRect()")
                            if (downCheck[u'width'] > 0):
                                downloadCheck=driver.find_element_by_id('download-checkbox')
                                try:
                                    downloadCheck.click()
                                    try:
                                        titl='pdfDDM'
                                        downloadMultiplePDFs=driver.find_element_by_class_name('related-articles__download')
                                        # print(downloadMultiplePDFs)
                                        downloadMultiplePDFs.click()
                                        time.sleep(.25)

                                        # Report on success of download
                                        toSend=[]
                                        toSend.append(cpc+'.Selenium.'+env+'.'+titl+'.count:1|c\n')
    
                                        statsD=''.join(toSend)
                                        # print('here is statsDdata')
                                        print(statsD+' '+Pii)

                                        try:
                                            # print('try to send UDP message')
                                            # print 
                                            UDPSock.sendto(statsD,addr)
                                        
                                        except:
                                            print('UDP send failed')
                                            pass

                                    except:
                                        print('no download multiple link found')
                                except:
                                    print('download-checkbox not clicked')
                            else:
                                print("downCheck[u'width'] not greater than zero")
                        except:
                            print "download-checkbox not found"

                    except:
                        print('no download link available')


                except urllib2.URLError:
                    time.sleep(.25)

                if artLoop > 0:
                    artLoop = artLoop-1
                    idx = idx+1

            browserLoop=browserLoop-1
            # print(browserLoop)

        idx=idx+1
        egress()

    except:
        print 'could not start browser'
        time.sleep(5)
