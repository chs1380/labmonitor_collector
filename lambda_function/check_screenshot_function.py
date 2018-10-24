import boto3
import json
import os
import datetime
from time import gmtime, strftime
import json


print('Loading function')
dynamodb_client = boto3.client('dynamodb')

def respond(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin' : '*',
            'Access-Control-Allow-Credentials' : 'true'
        },
    }


def lambda_handler(event, context):
    db = os.environ['ScreenshotMetaDataTable']
    student_id = event['pathParameters']['studentId']
    
    response = dynamodb_client.get_item(
        TableName=os.environ['ScreenshotMetaDataTable'],
        Key={'id': {"S": str(student_id)}})

    if "Item" not in response:
        return respond(None, {})
    
    data = json.loads(response['Item']['DetectedText']['S'])
    texts = list(map(lambda x: {"DetectedText": x["DetectedText"], "Type":x["Type"],"Confidence": x["Confidence"] }, data))  

    return respond(None, texts)
    