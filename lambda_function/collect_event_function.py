import boto3
import json
import os


print('Loading function')
s3 = boto3.client('s3')


def respond(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
        },
    }


def lambda_handler(event, context):
    print("Received lab event: " + json.dumps(event, indent=2))
    
    s3.put_object(Bucket=os.environ['StudentLabDataBucket'],Key='event.json',
              Body=json.dumps(event, indent=2),
          )
    return respond(None, "ok")
