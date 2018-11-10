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

def get_result(student_id:str, task:str):
    id = student_id + "-" + task    
    return dynamodb_client.get_item(
                TableName=os.environ['LabDataTable'],
                Key={'id': {"S": str(id)}})   

def lambda_handler(event, context):
    student_id = event['pathParameters']['studentId']
    
    text = get_result(student_id, "TextDetections")
    moderation = get_result(student_id, "ModerationLabels")
    celebrity = get_result(student_id, "CelebrityFaces")
    killed_processes = get_result(student_id, "KilledProecess")
    
    print(text)
    print(moderation)
    print(celebrity)
    print(killed_processes)
    
    texts = []
    moderations = []
    celebrities = []
    processes = []
    if "Item" in text:
        data = json.loads(text['Item']['DetectedText']['S'])
        line_data = filter(lambda x: x["Type"] == "LINE", data)
        texts = list(map(lambda x: {"DetectedText": x["DetectedText"]}, line_data))
    if "Item" in moderation:
        moderations = json.loads(moderation['Item']['ModerationLabels']['S'])
    if "Item" in celebrity:
        celebrities = json.loads(celebrity['Item']['CelebrityFaces']['S'])
        celebrities = list(map(lambda x: {"Name": x["Name"],"Urls":x["Urls"]}, celebrities))
    if "Item" in killed_processes:
        processes = json.loads(killed_processes['Item']['KilledProecess']['S'])
        

    result = {'texts': texts,'moderation': moderations, "celebrity": celebrities, "process": processes}
    return respond(None, result)
    