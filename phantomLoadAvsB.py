from subprocess import Popen
import sys
import urllib2
import time
import random

users=int(sys.argv[1])
PHOST=sys.argv[2]
duration=float(sys.argv[3])
renderArticles=sys.argv[4]
envM=sys.argv[5]
testDurationSecs=str(int(duration*3600))

# # Find hostname to use for passing to webdriver
# resp=urllib2.urlopen('http://169.254.169.254/latest/meta-data/public-hostname')
# PHOST=resp.read()
# PHOST='localhost'
# inst=urllib2.urlopen('http://169.254.169.254/latest/meta-data/instance-id')
# instID=inst.read()
# print(instID)

while users>0:
  if 'cert' in envM:
    idx=users%2
    if idx==0:
      env='cdc311'
    elif idx==1:
      env='cdc314'
  else:    	
    env='prod'
  #print 'I have entered the loop'
  ex=Popen('python ~/phantomRun.py '+PHOST+' '+testDurationSecs+' '+renderArticles+' '+env+ '&',shell=True,close_fds=True)
  users=users-1
  time.sleep(20)
	

