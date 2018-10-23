import boto3
import os
import sys
import uuid

rekognition_client = boto3.client('rekognition', region_name='us-east-1')
dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    db = os.environ['ScreenshotMetaDataTable']
    table = dynamodb.Table(os.environ['ScreenshotMetaDataTable'])
    
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key'] 
        
        response = rekognition_client.detect_text(
                        Image={
                            'S3Object': {
                                'Bucket': bucket,
                                'Name': key
                            }
                        }
                    )
        print(response)
        
        db_response = table.put_item(
           Item=response
        )
        
        print("PutItem succeeded:")
                
       
