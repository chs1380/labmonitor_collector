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
        },
    }


def lambda_handler(event, context):
    apiKey = apigateway.get_api_key(apiKey=event["requestContext"]["identity"]["apiKeyId"],includeValue=True)
    
    s3.put_object(Bucket=os.environ['StudentLabDataBucket'], Key="process_by_id/"+ apiKey["name"] + '/processstream.json',
              Body=event["body"],
              Metadata={"ip":event["requestContext"]["identity"]["sourceIp"], },
              ContentType="application/json"
          )

    
    now = datetime.datetime.now()
    partition = now.strftime("year=%Y/month=%m/day=%d/hour=%H")
    filename = now.strftime("processes_%M_%S.json")
    
    processes = json.loads(event["body"])
    body = []
    for student_event in processes:
        student_event["ip"] = event["requestContext"]["identity"]["sourceIp"]
        student_event["student"] = apiKey["description"]
        body.append(json.dumps(student_event) )
        
    s3.put_object(Bucket=os.environ['StudentLabDataBucket'], 
            Key = f"process_stream/{partition}/id={apiKey['name']}/{filename}",
            Body = '\n'.join(body).encode('utf8'),
            ContentType = "application/json"
          )
   
    return respond(None, os.environ['BlackListProcess'])
