#!/bin/bash

StudentMarkingBucket=$(aws cloudformation describe-stacks --stack-name $STACK_NAME --region $REGION \
--query 'Stacks[0].Outputs[?OutputKey==`StudentMarkingBucket`].OutputValue' --output text)
StudentLabDataBucket=$(aws cloudformation describe-stacks --stack-name $STACK_NAME --region $REGION \
--query 'Stacks[0].Outputs[?OutputKey==`StudentLabDataBucket`].OutputValue' --output text)
StudentScreenShotBucket=$(aws cloudformation describe-stacks --stack-name $STACK_NAME --region $REGION \
--query 'Stacks[0].Outputs[?OutputKey==`StudentScreenShotBucket`].OutputValue' --output text)
aws s3 rm s3://$StudentMarkingBucket  --recursive --region $REGION 
aws s3 rm s3://$StudentLabDataBucket  --recursive --region $REGION 
aws s3 rm s3://$StudentScreenShotBucket  --recursive --region $REGION 

KEY=id

TABLE_NAME=$(aws cloudformation describe-stacks --stack-name $STACK_NAME --region $REGION \
--query 'Stacks[0].Outputs[?OutputKey==`LabDataTable`].OutputValue' --output text)
aws dynamodb scan --table-name $TABLE_NAME --attributes-to-get "$KEY" \
  --query "Items[].$KEY.S" --output text --region $REGION| \
  tr "\t" "\n" | \
  xargs -t -I keyvalue aws dynamodb delete-item --table-name $TABLE_NAME \
  --key "{\"$KEY\": {\"S\": \"keyvalue\"}}" --region $REGION
  
TABLE_NAME=$(aws cloudformation describe-stacks --stack-name $STACK_NAME --region $REGION \
--query 'Stacks[0].Outputs[?OutputKey==`ConversationTable`].OutputValue' --output text)
aws dynamodb scan --table-name $TABLE_NAME --attributes-to-get "$KEY" \
  --query "Items[].$KEY.S" --output text --region $REGION | \
  tr "\t" "\n" | \
  xargs -t -I keyvalue aws dynamodb delete-item --table-name $TABLE_NAME \
  --key "{\"$KEY\": {\"S\": \"keyvalue\"}}" --region $REGION