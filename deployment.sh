aws s3api create-bucket --bucket cywonglabcollectorsourcebucket1 --region ap-southeast-1 --create-bucket-configuration LocationConstraint=ap-southeast-1
cp lambda_function/* venv/lib/python3.6/dist-packages
rm package.yaml
sam package --template-file template.yaml --s3-bucket cywonglabcollectorsourcebucket1 --output-template-file package.yaml

aws cloudformation deploy --stack-name labmonitor --template-file package.yaml --capabilities CAPABILITY_IAM \
--parameter-overrides \
    RunUnitTest="true" \
    GitCommand="git clone -b server https://github.com/wongcyrus/ite3101_introduction_to_programming.git" \
    SourceRespositoryName="ite3101_introduction_to_programming"
