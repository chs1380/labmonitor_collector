
StudentMarkingBucket=$(aws cloudformation describe-stacks --stack-name assignmentmonitor \
--query 'Stacks[0].Outputs[?OutputKey==`StudentMarkingBucket`].OutputValue' --output text)
StudentLabDataBucket=$(aws cloudformation describe-stacks --stack-name assignmentmonitor \
--query 'Stacks[0].Outputs[?OutputKey==`StudentLabDataBucket`].OutputValue' --output text)
aws s3 rm s3://$StudentMarkingBucket  --recursive
aws s3 rm s3://$StudentLabDataBucket  --recursive
aws cloudformation delete-stack --stack-name assignmentmonitor
