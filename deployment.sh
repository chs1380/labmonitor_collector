aws s3api create-bucket --bucket cywonglabcollectorsourcebucket --region us-east-1
sam package --template-file template.yaml --s3-bucket cywonglabcollectorsourcebucket --output-template-file package.yaml
aws cloudformation deploy --template-file package.yaml --stack-name labmonitor --capabilities CAPABILITY_IAM