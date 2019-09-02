import sys
sys.path.append("/opt/")
import boto3
import json
import os
import datetime


print('Loading function')
s3 = boto3.client('s3')
apigateway = boto3.client('apigateway')
kinesis = boto3.client('kinesis')

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
    s3.put_object(Bucket=os.environ['StudentLabDataBucket'], Key="event_by_id/"+ student_id + '/eventstream.json',
              Body=event["body"],
              Metadata={"ip":event["requestContext"]["identity"]["sourceIp"], },
              ContentType="application/json"
          )
    
    now = datetime.datetime.now()
    partition = now.strftime("year=%Y/month=%m/day=%d/hour=%H")
    filename = now.strftime("events_%M_%S.json")
    
    events = json.loads(event["body"])
    body = []
    
    keybroad = []
    mouse = []
    count = 0
    for student_event in events:
        student_event["ip"] = event["requestContext"]["identity"]["sourceIp"]
        student_event["student"] = apiKey["description"]
        body.append(json.dumps(student_event) )
        
        if os.environ['EnableRealtimeAnalystics'] == 'true':
            del (student_event['ip'], student_event['student'])
            student_event['id'] = student_id
            if ((student_event["name"] == "KeyPressEvent") or (student_event["name"] == "KeyReleaseEvent")):
                keybroad.append({'Data': json.dumps(student_event).encode(), 'PartitionKey':student_id})
                count += 1
            else:
                mouse.append({'Data': json.dumps(student_event).encode(), 'PartitionKey':student_id})
                count += 1
                
            if count == 500:
                put_record_to_kinesis(mouse, os.environ['MouseEventStream'])
                put_record_to_kinesis(keybroad, os.environ['KeybroadEventStream'])
                mouse = []
                keybroad = []
                count = 0
    
    if os.environ['EnableRealtimeAnalystics'] == 'true':        
        put_record_to_kinesis(mouse, os.environ['MouseEventStream'])
        put_record_to_kinesis(keybroad, os.environ['KeybroadEventStream'])   
        
    s3.put_object(Bucket=os.environ['StudentLabDataBucket'], 
            Key = f"event_stream/{partition}/id={student_id}/{filename}",
            Body = '\n'.join(body).encode('utf8'),
            ContentType = "application/json"
          )
   
    return respond(None, student_id + f" saved {len(events)} events.")
    
def put_record_to_kinesis(events, stream_name):
    if(len(events) > 0):
        response = kinesis.put_records(Records=events, StreamName=stream_name)
        print(response)
        