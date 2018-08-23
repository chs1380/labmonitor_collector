aws s3api create-bucket --bucket cywonglabcollectorsourcebucket1 --region ap-southeast-1 --create-bucket-configuration LocationConstraint=ap-southeast-1
cp lambda_function/* venv/lib/python3.6/dist-packages
rm package.yaml
sam package --template-file template.yaml --s3-bucket cywonglabcollectorsourcebucket1 --output-template-file package.yaml
aws cloudformation deploy --template-file package.yaml --stack-name labmonitor --capabilities CAPABILITY_IAM