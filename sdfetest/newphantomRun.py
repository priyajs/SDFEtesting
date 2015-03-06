#import subprocess
from subprocess import Popen, PIPE
import sys
import urllib2
import time
import csv
import random
import socket

env=sys.argv[1]
duration=int(sys.argv[2])
renderArticles=sys.argv[3]

#statsDHost='ec2-54-80-6-76.compute-1.amazonaws.com'
statsDHost='statsd.elsst.com'
#---Handling region ----#
availzone=urllib2.urlopen('http://169.254.169.254/latest/meta-data/placement/availability-zone')
zone=availzone.read()
#zone='eu-west-1'
#print(zone)
if(zone.find('eu-west-1') > -1):
 #print 'eu-west-1'
 region='EUW1'
 
if(zone.find('us-east-1') > -1):
 #print 'us-east-1'
 region='USE1'
if(zone.find('us-west-2') > -1):
 #print 'us-west-2'
 region='USW2'
if(zone.find('ap-southeast-1') > -1):
 #print 'ap-southeast-1'
 region='APSE1'

print(region)

PII=[]
try:
 csvRd = csv.reader(open('/home/ubuntu/sdfePIIwhitelist.csv','rb'))
 piiCount = 4320
except:
 csvRd = csv.reader(open('C:/Scripts/whitelist_piis.csv','rb'))
 piiCount = 1000000
for j in csvRd:
 PII.append(j)
 
UDPSock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
## statsd host & port
addr=(statsDHost,8125)



#Define end of test based on input above
endTime = int(time.time()+duration)
#endTime = int(time.time()+30)

try:
 if(env.find('sdfe') > -1):
  envS=env.split('.')
  envPrint=envS[0]
 elif(env.find('cdc') > -1):
  envPrint=env
 elif(env.find('new') > -1):
  envPrint='sdnew'
 else:
  envPrint='sd'
except:
 envPrint=env

while endTime > int(time.time()):
 l=[]
 loop=5
 while loop>0:
  #idx = int(random.random()*piiCount)
  #idxPii=idx
  #print('articleIDX:'+str(idx))
  #print('sd.article.phantom.'+envPrint+'.'+region+'.total:1|c\n')
  print(envPrint)
  idx=random.randrange(0,4320,1)
  inputPII=str(PII[idx]).strip('[\']')
  #inputPII='S0008874905000535'
  print(inputPII)
  #print 'I am trying the phantomJS request now'
  #ex=Popen('phantomjs article.js '+hostNm+' '+inputPII+' '+renderArticles,stdout=PIPE)#,close_fds=True,shell=True)
  l.append('sd.article.phantom.'+envPrint+'.'+region+'.total:1|c\n')
  l.append('sd.article.phantom.'+envPrint+'.total:1|c\n')
  print('sd.article.phantom.'+envPrint+'.'+region+'.total:1|c\n')
  ex=Popen(['phantomjs', 'article.js',env,inputPII,renderArticles],stdout=PIPE)#,close_fds=True,shell=True)
  exOut=ex.communicate()
  #print('ex.communicate below:')
  #print(exOut)
  #print(exOut[0])
  #print(inputPII)
  try:
   #print('find duration')
   exS=exOut[0].split(' ')
   lt=exS[0].split(':')[1]
   tt=exS[1].split(':')[1]
   #print tt[0:tt.index('ms')]
   #print lt[0:lt.index('ms')]
   msTtlb= tt[0:tt.index('ms')]
   msLoad=lt[0:lt.index('ms')]
   #Regional
   l.append('sd.article.phantom.'+envPrint+'.'+region+'.load:'+msLoad+'|ms\n')
   l.append('sd.article.phantom.'+envPrint+'.'+region+'.ttlb:'+msTtlb+'|ms\n')
   l.append('sd.article.phantom.'+envPrint+'.'+region+'.pass:1|c\n')
   #Global
   l.append('sd.article.phantom.'+envPrint+'.load:'+msLoad+'|ms\n')
   l.append('sd.article.phantom.'+envPrint+'.ttlb:'+msTtlb+'|ms\n')
   l.append('sd.article.phantom.'+envPrint+'.pass:1|c\n')
  except:
   print('something wrong with article: '+inputPII+' '+exOut[0])
   try:
    if exOut[0].index('Error'):
	 l.append('sd.article.phantom.'+envPrint+'.'+region+'.fail:1|c\n')
	 l.append('sd.article.phantom.'+envPrint+'.fail:1|c\n')
   except:
    pass
  time.sleep(.25)
  loop=loop-1
  
 statsDdata=''.join(l)
 #print(statsDdata)
 UDPSock.sendto(statsDdata,addr)