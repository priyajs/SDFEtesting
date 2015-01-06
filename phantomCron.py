from subprocess import Popen,PIPE
import sys
import urllib2
import time
import random

inst=urllib2.urlopen('http://169.254.169.254/latest/meta-data/instance-type')
instType=inst.read()

ex=Popen('ps -ef|grep -c phantomRun.py',shell=True,stdout=PIPE)
count=ex.communicate()[0]
running=int(count.splitlines()[0])-1

if '.xlarge' in instType:
   total=20
if '.large' in instType:
   total=8  
#remove
total=4
#end remove
toRun=total-running-1

print 'toRun: '+str(toRun)

if toRun > 1:
  ex=Popen('python phantomLoadPvsS.py '+str(toRun)+' 6 0',shell=True,close_fds=True)


