import boto3
import json
import os
import datetime
from time import gmtime, strftime
import json


print('Loading function')
dynamodb = boto3.resource('dynamodb')

def respond(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
        },
    }


def lambda_handler(event, context):
    db = os.environ['ScreenshotMetaDataTable']
    table = dynamodb.Table(os.environ['ScreenshotMetaDataTable'])
    student_id = event['pathParameters']['studentId']

    now = datetime.datetime.now()
    partition = now.strftime("%Y/%m/%d/%H/%M")
    id = f"{student_id}-{partition}"
    print(str(id))
    response = table.get_item(Key={'id': str(id)})
    if "Item" not in response:
        return respond(None, {})
    return respond(None, response['Item'])
    