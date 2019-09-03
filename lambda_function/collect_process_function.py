import sys
sys.path.append("/opt/")
import boto3
import json
import os
import datetime


print('Loading function')
s3 = boto3.client('s3')
apigateway = boto3.client('apigateway')
dynamodb = boto3.resource('dynamodb')

def save_to_dyanmodb(student_id:str, task:str, key:str, suffix:str, data):
    id = f"{student_id}-{task}-{suffix}"
    item ={"id": id, key: json.dumps(data)}
    table = dynamodb.Table(os.environ['LabDataTable'])
    db_response = table.put_item(
       Item=item
    )
    id = f"{student_id}-{task}"
    item ={"id": id, key: json.dumps(data)}
    db_response = table.put_item(
       Item=item
    )

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
    
    student_id = apiKey["name"].split("_")[0]
    s3.put_object(Bucket=os.environ['StudentLabDataBucket'], Key="process_by_id/"+ student_id + '/processstream.json',
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
        
    killed_processes = list(filter(lambda x: x["is_killed"], processes))
    if len(killed_processes) > 0:
        killed_process_names = list(set(list(map(lambda x: x["name"], killed_processes))))
        suffix = datetime.datetime.now().strftime("%Y/%m/%d/%H/%M/%S")
        save_to_dyanmodb(student_id, "KilledProecess", "KilledProecess", suffix, killed_process_names)
    
    s3.put_object(Bucket=os.environ['StudentLabDataBucket'], 
            Key = f"process_stream/{partition}/id={student_id}/{filename}",
            Body = '\n'.join(body).encode('utf8'),
            ContentType = "application/json"
          )
   
    return respond(None, os.environ['DataSaving'] +","+ os.environ['BlackListProcess'])
