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
import socket

#------------------------------------------------------------
#--- Get Interactive Input for number of loops to execute ---
numLoops = int(sys.argv[1])

#--- Browser definition for Grid usage ----------
browser = sys.argv[2]

#--- SeGrid Hub designation --------------------
hub = sys.argv[3]

env = sys.argv[4]
#env = 'qa.sdfe'

statsDHost='statsd.elsst.com'
"""
  Define UDP connection to send data to statsD
"""
UDPSock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
## statsd host & port
addr=(statsDHost,8125)


#--- Read List of PIIs -----------------
PII=[]
try:
  #csvRd = csv.reader(open('/home/ubuntu/PIIs_250k.csv','rb'))
  csvRd = csv.reader(open('/home/ubuntu/sdfePIIwhitelist.csv','rb'))
  piiCount = 4300
except:
  csvRd = csv.reader(open('C:/Scripts/whitelist_piis.csv','rb'))
  piiCount = 4300
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
    print ("----URLError - pass? ----")
    pass
  except:
    print ("--- Other Error on Exit -----")
    pass

#------------------------------------------------------
#       Function to execute a request or page interaction
#               handles associated error conditions
#               Makes call to collect page timing
#-------------
def getPage(resource):
  try:
    #print ('getting resource')
    resource
    if 'Unable to process' in driver.title:
      print 'Error - Unable to process, wait 60 seconds'
      time.sleep(60)
      pass
    elif 'Error' in driver.title:
      print 'Error, wait 60 seconds'
      time.sleep(60)
      pass
    elif 'Page Not Found' in driver.title:
      print 'Error, wait 60 seconds'
      time.sleep(60)
      pass
    else:
      #print ('getting metrics')
      metricsCollect(titl,'NA')
      cnt='sd.article.se.'+envPrint+'.pass:1|c\n'

      # Send data to graphite
      UDPSock.sendto(cnt,addr)

      time.sleep(.25)
  except urllib2.URLError:
    print 'URLError'
    pass
  except:
    print ('unknown failure for: '+titl)
    pass

#-------------------------------------------------------
#       Function to capture various page timing metrics
#               and output to screen for log tailing and troubleshooting
#---------------
def metricsCollect(dtitl,ID):
  l=[]
  try:
    navS = driver.execute_script("return performance.timing.navigationStart")
    respS = driver.execute_script("return performance.timing.responseStart")
    respE = driver.execute_script("return performance.timing.responseEnd")
    dom = driver.execute_script("return performance.timing.domInteractive")
    loadE = driver.execute_script("return performance.timing.loadEventEnd")
    domCL = driver.execute_script("return performance.timing.domContentLoadedEventEnd")
    if loadE > navS:
      pgLoad = str(int(loadE-navS))
      domI = str(int(dom-navS))
      cont = str(int(respE-navS))
      ttfb = str(int(respS-navS))
      sr = str(int(domCL-navS))
      #print('\nperf details found\n')
      l.append('sd.article.se.'+envPrint+'.load:'+pgLoad+'|ms\n')
      l.append('sd.article.se.'+envPrint+'.pgi:'+domI+'|ms\n')
      l.append('sd.article.se.'+envPrint+'.ttlb:'+cont+'|ms\n')
      l.append('sd.article.se.'+envPrint+'.ttfb:'+ttfb+'|ms\n')
      l.append('sd.article.se.'+envPrint+'.sr:'+sr+'|ms\n')

      # Send data to graphite
      statsDdata=''.join(l)
      #print(statsDdata)
      UDPSock.sendto(statsDdata,addr)
    else:
        pgLoad = 'NA'
        cont='NA'
        ttfb = 'NA'
        #print('perf details NOT found')

    # Datetime for Timestamp
    dt = datetime.datetime.now()
    dTm = str(dt.strftime("%Y/%m/%d %H:%M:%S%Z"))

    #print(browser+'\t'+dTm+'\t'+ttfb+'\t'+cont+'\t'+pgLoad)

  #
  # End metricsCollect()
  #
  except:
      pass


#=============================================================
#-------------------------------------------------------------
#       Script Begins Here
#-------------------------------------------------------------
#=============================================================

#--- Define static Article Value for looping
idx=0
loop=1
while numLoops > loop:
  #print('iteration: '+str(loop)+' browser:'+browser)
  """
  Define capabilities of remote webdriver
  Specifically: assign browser type
  """
  try:
    #print('loading browser')
    driver=webdriver.Remote("http://"+hub+":4200/wd/hub",desired_capabilities={"browserName": browser})
    #driver=webdriver.Chrome()
    #print('wait for it...')
    #print datetime.datetime.now()
    time.sleep(1)

    #-------------------------------------------------
    #       Define baseURL for following transactions
    #-------------------------------------------------
    if(env.find('sdfe') > -1):
      envS=env.split('.')
      baseURL='www.'+env+'.sciencedirect.com'
      base='sdfe'
      envPrint='FE'+envS[0]
      """
      if (env == 'prod.sdfe'):
        baseURL = 'www.prod.sdfe.sciencedirect.com'
        base='sdfe'
        envPrint='FEprod'
      if (env == 'perf.sdfe'):
        baseURL = 'www.perf.sdfe.sciencedirect.com'
        base='sdfe'
        envPrint='FEperf'
      """
    elif(env.find('cdc') > -1):
        baseURL = env+'-www.sciencedirect.com'
        base=env
        envPrint=env
    else:
      baseURL = 'www.sciencedirect.com'
      base='sd'
      envPrint='sd'


    #baseURL = 'www.perf.sdfe.sciencedirect.com'
    #base='sdfe'
    #envPrint='FEperf'

    # Navigate to "home page" for context only if its prod.sdfe
    if(envPrint=='FEprod'):
      try:
        driver.get('http://'+baseURL)
        time.sleep(.5)
        # Add cookie to allow non-loading of site catalyst
        #if(envPrint=='FEprod'):
        try:
          driver.add_cookie({'name':'TestTrafficDriver','value':'selenium'})
        except:
          print 'could not add cookie'
          pass
      except:
        print 'could not find home'
        pass


    #-------------------------------------------------
    #      Add looping structure to minimize browser churn
    #-------------------------------------------------
    browserLoop=0
    while(browserLoop < 20):
    #while(browserLoop < 5):
      #print ('browserLoop: '+str(browserLoop))
      #--- Define Random Value ---------------
      idx = int(random.random()*piiCount)
      idxPii=idx
      Pii=str(PII[idxPii]).strip('[\']')
      titl='Content Delivery'
      if (browserLoop == 0 and base=='sdfe' and (env != 'prod.sdfe' and env != 'qa.sdfe')):
          #print('sdfe, take 1')
          url="http://sdfe-engineers:Target947Tirpitz@"+baseURL+"/science/article/pii/"+Pii
      else:
        url="http://"+baseURL+"/science/article/pii/"+Pii
      print str(idx)+' '+Pii+' '+url
      getPage(driver.get(url))
      time.sleep(random.uniform(12.5,16.5))
      browserLoop+=1

    #print(browserLoop)
    loop += 1
    egress()
    time.sleep(random.uniform(30,45))

  except:
    print('loading browseri or other failed')
    print datetime.datetime.now()
    time.sleep(5)
    pass


