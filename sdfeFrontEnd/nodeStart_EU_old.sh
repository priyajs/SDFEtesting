#/bin/bash
sleep 10

sudo pkill chrome

sudo xvfb-run --server-args='+extension RANDR -screen 0 1280x800x24' java -jar /home/ubuntu/selenium-server.jar -role node -browser browserName=chrome,maxInstances=6 -maxSession 6 -port 4320 -hub http://sdfe-se-1511439383.eu-west-1.elb.amazonaws.com/grid/register -registerCycle 5000 &
