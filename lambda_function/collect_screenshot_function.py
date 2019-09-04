import sys
sys.path.append("/opt/")
import boto3
import json
import os
import datetime

from helper import *

print('Loading function')
s3 = boto3.client('s3')
apigateway = boto3.client('apigateway')


def lambda_handler(event, context):
    if os.environ['TakeScreenShot'] == "false":
        print("TakeScreenShot Disabled!")
        return respond(None, "Disabled")
    
    apiKey = apigateway.get_api_key(apiKey=event["requestContext"]["identity"]["apiKeyId"],includeValue=True)
    student_id = apiKey["name"].split("_")[0]

    now = datetime.datetime.now()
    partition = now.strftime("year=%Y/month=%m/day=%d/hour=%H")
    filename = now.strftime("Screenshot_%M_%S.jpeg")

    bucket = os.environ['StudentScreenShotBucket']
    key = f"screenshot/{partition}/id={student_id}/{filename}"
   
    conditions = [
        ['content-length-range', 0, 524289]
    ]

    signed_url = s3.generate_presigned_post(Bucket=bucket, Key=key, Conditions=conditions, ExpiresIn=60*2,)
    return respond(None, {"screen_capture_period":os.environ['ScreenCapturePeriod'], "signed_url":signed_url})
    