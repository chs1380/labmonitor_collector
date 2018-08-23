import boto3

apigateway = boto3.client('apigateway')
apiKey = apigateway.get_api_key(apiKey="ckuyhjlsk7",includeValue=True)
print(apiKey["name"])