sourcebucket=cywongit3101assignemnt1718
aws s3api create-bucket --bucket $sourcebucket --region ap-southeast-1 --create-bucket-configuration LocationConstraint=ap-southeast-1
cp lambda_function/* venv/lib/python3.6/dist-packages
rm package.yaml
sam package --template-file template.yaml --s3-bucket $sourcebucket --output-template-file package.yaml

aws cloudformation deploy --stack-name labmonitor --template-file package.yaml --capabilities CAPABILITY_IAM \
--parameter-overrides \
    RunUnitTest="true" \
    GitCommand="git clone https://username:url_encode_password@git-codecommit.ap-southeast-1.amazonaws.com/v1/repos/lab_checker" \
    SourceRespositoryName="lab_checker"
