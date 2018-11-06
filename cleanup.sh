StudentMarkingBucket=$(aws cloudformation describe-stacks --stack-name $STACK_NAME --region $REGION \
--query 'Stacks[0].Outputs[?OutputKey==`StudentMarkingBucket`].OutputValue' --output text)
StudentLabDataBucket=$(aws cloudformation describe-stacks --stack-name $STACK_NAME --region $REGION \
--query 'Stacks[0].Outputs[?OutputKey==`StudentLabDataBucket`].OutputValue' --output text)
StudentScreenShotBucket=$(aws cloudformation describe-stacks --stack-name $STACK_NAME --region $REGION \
--query 'Stacks[0].Outputs[?OutputKey==`StudentScreenShotBucket`].OutputValue' --output text)
aws s3 rm s3://$StudentMarkingBucket  --recursive --region $REGION 
aws s3 rm s3://$StudentLabDataBucket  --recursive --region $REGION 
aws s3 rm s3://$StudentScreenShotBucket  --recursive --region $REGION 
sleep 10
aws cloudformation delete-stack --stack-name $STACK_NAME --region $REGION