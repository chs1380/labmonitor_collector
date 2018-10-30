echo "Deploy $STACK_NAME stack"

sourcebucket=cywong$STACK_NAME
aws s3 mb s3://$sourcebucket --region $REGION
cp lambda_function/* venv/lib/python3.6/dist-packages
rm package.yaml
sam package --template-file template.yaml --s3-bucket $sourcebucket --output-template-file package.yaml

aws cloudformation deploy --stack-name $STACK_NAME --template-file package.yaml \
--region $REGION --capabilities CAPABILITY_IAM \
--parameter-overrides \
    RunUnitTest="true" \
    GitCommand="git clone -b server https://github.com/wongcyrus/ite3101_introduction_to_programming.git" \
    SourceRespositoryName="ite3101_introduction_to_programming" \
    EnableRealtimeAnalystics="true" \
    CalendarUrl="https://calendar.google.com/calendar/ical/spe8ehlqjkv8hd7mdjs3d2g80c%40group.calendar.google.com/public/basic.ics" \
    CourseKeywords="Introduction to Programing"
