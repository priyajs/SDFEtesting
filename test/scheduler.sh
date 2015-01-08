#!/bin/bash
#
# This will delete and create a CF stack being used for SDFE
#
# testing with describe regions
LOGFILE="/var/log/scheduler-messages.log" 
#
aws ec2 describe-regions --region us-west-2 >> $LOGFILE
# delete the existing stack
#
#echo "`date` deleting CF stack" >> $LOGFILE
#aws cloudformation delete-stack --stack-name cron-sdfe --region us-west-2
#
#
# wait for stack deletion to complete
#
#echo "`date` waiting for CF stack delete to complete....." >> $LOGFILE
#sleep 10m
#
# start new stack
#
#echo "`date` creating new stack" >> $LOGFILE
#aws cloudformation create-stack --stack-name cron-sdfe --template-url https://s3-us-west-2.amazonaws.com/sdfe-testresources/test/cronServer.template  --parameters ParameterKey=KeyName,ParameterValue=awsPerfTest --region us-west-2
