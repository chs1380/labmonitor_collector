StudentMarkingBucket=$(aws cloudformation describe-stacks --stack-name $STACK_NAME \
--query 'Stacks[0].Outputs[?OutputKey==`StudentMarkingBucket`].OutputValue' --output text)
StudentLabDataBucket=$(aws cloudformation describe-stacks --stack-name $STACK_NAME \
--query 'Stacks[0].Outputs[?OutputKey==`StudentLabDataBucket`].OutputValue' --output text)
StudentScreenShotBucket=$(aws cloudformation describe-stacks --stack-name $STACK_NAME \
--query 'Stacks[0].Outputs[?OutputKey==`StudentScreenShotBucket`].OutputValue' --output text)
aws s3 rm s3://$StudentMarkingBucket  --recursive
aws s3 rm s3://$StudentLabDataBucket  --recursive
aws s3 rm s3://$StudentScreenShotBucket  --recursive
sleep 10
aws cloudformation delete-stack --stack-name $STACK_NAME