#/bin/bash
sudo pkill python&
sudo pkill chrome&
sudo pkill chromedriver& 
sudo pkill xvfb&
sudo killall Xvfb&
sudo kill $(ps aux|grep [j]ava|grep maxInstances|awk '{print $2}') 

sudo xvfb-run --server-args='+extension RANDR -screen 0 1280x800x24' java -jar /home/ubuntu/selenium-server.jar -role node -browser browserName=chrome,maxInstances=10 -maxSession 10 -port 4320 -hub http://localhost:4200/grid/register -registerCycle 5000 &
