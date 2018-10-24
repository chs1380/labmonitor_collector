import boto3
import json
import os
import datetime


print('Loading function')
s3 = boto3.client('s3')
apigateway = boto3.client('apigateway')


def respond(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
        }
    }


def lambda_handler(event, context):
    apiKey = apigateway.get_api_key(apiKey=event["requestContext"]["identity"]["apiKeyId"],includeValue=True)
    student_id = apiKey["name"].split("_")[0]

    now = datetime.datetime.now()
    partition = now.strftime("year=%Y/month=%m/day=%d/hour=%H")
    filename = now.strftime("Screenshot_%M_%S.jpg")

    bucket = os.environ['StudentScreenShotBucket']
    key = f"screenshot/{partition}/id={student_id}/{filename}"
   

    conditions = [
        ['content-length-range', 0, 3000000]
    ]

    signed_url = s3.generate_presigned_post(Bucket=bucket, Key=key, Conditions=conditions, ExpiresIn=60*2,)
    return respond(None, signed_url)
    