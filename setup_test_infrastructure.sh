#!/usr/bin/env bash

if [[ "$1" == "--create-stack" ]]
then
  aws cloudformation create-stack --stack-name TestAnsibleProxyPlayback --template-body file://cloudformation.yml --output json || true
  status=`aws cloudformation describe-stacks --stack-name TestAnsibleProxyPlayback --query Stacks[0].StackStatus --output text`
  while [[ "$status" == "CREATE_IN_PROGRESS" ]]
  do
    sleep 10;
    status=`aws cloudformation describe-stacks --stack-name TestAnsibleProxyPlayback --query Stacks[0].StackStatus --output text`
  done
  aws cloudformation describe-stacks --stack-name TestAnsibleProxyPlayback --query Stacks[0].Outputs --output json > ansible/tests/config.json
else
  ChangeSetId=`aws cloudformation create-change-set --stack-name TestAnsibleProxyPlayback --change-set-name TestAnsibleProxyPlaybackCS --template-body file://cloudformation.yml --output text --query Id`
  status=`aws cloudformation describe-change-set  --change-set-name $ChangeSetId  --query Status --output text`
  while [[ "$status" == "CREATE_IN_PROGRESS" ]]
  do
    sleep 10;
    status=`aws cloudformation describe-change-set  --change-set-name $ChangeSetId  --query Status --output text`
  done
  aws cloudformation execute-change-set --change-set-name $ChangeSetId  --output json
  status=`aws cloudformation describe-change-set  --change-set-name $ChangeSetId  --output text --query Status`
  while [[ "$status" != "CREATE_COMPLETE" ]]
  do
    echo "Status: $status "
    sleep 10;
    status=`aws cloudformation describe-change-set  --change-set-name $ChangeSetId  --query Status --output text`
  done
  aws cloudformation describe-stacks --stack-name TestAnsibleProxyPlayback --query Stacks[0].Outputs --output json > ansible/tests/config.json
fi
# --capabilities  CAPABILITY_IAMb