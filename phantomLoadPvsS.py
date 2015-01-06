from subprocess import Popen
import sys
import urllib2
import time
import random

users=int(sys.argv[1])
duration=float(sys.argv[2])
renderArticles=sys.argv[3]


testDurationSecs=str(int(duration*3600))

# # Find hostname to use for passing to webdriver
# resp=urllib2.urlopen('http://169.254.169.254/latest/meta-data/public-hostname')
# PHOST=resp.read()
# PHOST='localhost'
# inst=urllib2.urlopen('http://169.254.169.254/latest/meta-data/instance-id')
# instID=inst.read()
# print(instID)

while users>0:
  """
  if 'cert' in envM:
    idx=users%2
    if idx==0:
      env='cdc311'
    elif idx==1:
      env='cdc314'
  else:    	
    env='prod'
  """
  #envs=['banana.sdfe','cdc314']
  envs=['perf.sdfe','cdc314']
  for env in envs:
    ex=Popen('python ~/phantomRun.py '+env+' '+testDurationSecs+' '+renderArticles+'&',shell=True,close_fds=True)
  users=users-2
  time.sleep(20)
	

