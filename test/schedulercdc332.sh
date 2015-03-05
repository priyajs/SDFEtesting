#!/bin/bash
#
# This will delete and create a CF stack being used for SDFE
#
# testing with describe regions
LOGFILE="/var/log/scheduler-messages.log" 
#
#aws ec2 describe-regions --region us-west-2 >> $LOGFILE
# delete the existing stack in us-west-2
#
echo "`date` deleting CF stack cdc332soaktest-VPC us-west-2" >> $LOGFILE
aws cloudformation delete-stack --stack-name cdc332soaktest-VPC --region us-west-2
#
#
# wait for stack deletion to complete
#
echo "`date` waiting for CF stack delete to complete....." >> $LOGFILE
sleep 5m
#
# start new stack 
#
echo "`date` creating new stack cdc332soaktest-VPC us-west-2" >> $LOGFILE
aws cloudformation create-stack --stack-name cdc332soaktest-VPC --template-url https://s3-us-west-2.amazonaws.com/sdfe-testresources/test/SDFE-SeGrid-20141222-VPC-usw2-cdc332.template  --parameters ParameterKey=MaxASGSize,ParameterValue=1 --capabilities CAPABILITY_IAM --region us-west-2
sleep 5m
# delete the existing stack in ap-southeast-1
#
echo "`date` deleting CF stack cdc332soaktest ap-southeast-1" >> $LOGFILE
aws cloudformation delete-stack --stack-name cdc332soaktest --region ap-southeast-1
#
#
# wait for stack deletion to complete
#
echo "`date` waiting for CF stack delete to complete....." >> $LOGFILE
sleep 5m
#
# start new stack 
#
echo "`date` creating new stack cdc332soaktest ap-southeast-1" >> $LOGFILE
aws cloudformation create-stack --stack-name cdc332soaktest --template-url https://s3-us-west-2.amazonaws.com/sdfe-testresources/sdfeFrontEnd/SDFE-SeGrid-20141022-se1-cdc332.template  --parameters ParameterKey=MaxASGSize,ParameterValue=1 --capabilities CAPABILITY_IAM --region ap-southeast-1
# delete the existing stack in eu-west-1
#
sleep 5m
echo "`date` deleting CF stack cdc332soaktest eu-west-1" >> $LOGFILE
aws cloudformation delete-stack --stack-name cdc332soaktest --region eu-west-1
#
#
# wait for stack deletion to complete
#
echo "`date` waiting for CF stack delete to complete....." >> $LOGFILE
sleep 5m
#
# start new stack 
#
echo "`date` creating new stack cdc332soaktest eu-west-1" >> $LOGFILE
aws cloudformation create-stack --stack-name cdc332soaktest --template-url https://s3-us-west-2.amazonaws.com/sdfe-testresources/sdfeFrontEnd/SDFE-SeGrid-20141022-EU-cdc332.template  --parameters ParameterKey=MaxASGSize,ParameterValue=1 --capabilities CAPABILITY_IAM --region eu-west-1