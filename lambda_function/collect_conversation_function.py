import sys
sys.path.append("/opt/")
import boto3
import json
import os
import datetime
import urllib


print('Loading function')
s3 = boto3.client('s3')
comprehend = boto3.client('comprehend')
dynamodb = boto3.resource('dynamodb')


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

def save_to_dyanmodb(student_id:str, task:str, key:str, suffix:str, data):
    id = f"{student_id}-{task}-{suffix}"
    item ={"id": id, key: json.dumps(data)}
    table = dynamodb.Table(os.environ['ConversationTable'])
    db_response = table.put_item(
       Item=item
    )
    id = f"{student_id}-{task}"
    item ={"id": id, key: json.dumps(data)}
    db_response = table.put_item(
       Item=item
    )

def lambda_handler(event, context):
    student_id = event['pathParameters']['studentId']
    text = urllib.parse.unquote(event['pathParameters']['text'])

    now = datetime.datetime.now()
    partition = now.strftime("year=%Y/month=%m/day=%d/hour=%H")

    sentiment_response = comprehend.detect_sentiment(
        Text=text,
        LanguageCode='en'
    )
    
    suffix = datetime.datetime.now().strftime("%Y/%m/%d/%H/%M/%S")
    data = {'text': text , "sentiment": sentiment_response}
    save_to_dyanmodb(student_id, "Sentiment", "Sentiment", suffix, data)

    return respond(None, [student_id,text])
    