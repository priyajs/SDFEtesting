#!/bin/bash
#
# This will delete and create a CF stack phantomperf test being used for SDFE

#LOGFILE="/l-n/log/elsevier/startGrid.log"

#
# delete the existing stack
#
echo "`date` deleting CF stack" 
aws cloudformation delete-stack --stack-name perfphantomtest --region us-west-2

#
# wait for stack deletion to complete
#
echo "`date` waiting for CF stack delete to complete....." 
sleep 10m

#
# start new stack
#
echo "`date` creating new stack" 
aws cloudformation create-stack --stack-name perfphantomtest --template-url https://s3-us-west-2.amazonaws.com/sdfe-testresources/sdfetest/SDFE_phantomJS_20141022-SDFE_perf.template  --parameters ParameterKey=MaxASGSize,ParameterValue=1 --region us-west-2


