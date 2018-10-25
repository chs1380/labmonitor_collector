import boto3
import os
import sys
import uuid
import urllib.parse
import json

rekognition_client = boto3.client('rekognition', region_name='us-east-1')
dynamodb = boto3.resource('dynamodb')
s3 = boto3.client('s3')

def lambda_handler(event, context):
    db = os.environ['ScreenshotMetaDataTable']
    table = dynamodb.Table(os.environ['ScreenshotMetaDataTable'])
    
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']

        download_path = '/tmp/{}.jpeg'.format(uuid.uuid4())
        
        key = urllib.parse.unquote(key)
        s3.download_file(bucket, key, download_path)
        with open(download_path, 'rb') as image:
            response = rekognition_client.detect_text(Image={'Bytes': image.read()})
     
        detected_text = response['TextDetections']
        segment = key.split("/")
        student_id =segment[5].split("=")[1]
        year = segment[1].split("=")[1]
        month =  segment[2].split("=")[1]
        day =  segment[3].split("=")[1]
        hour =  segment[4].split("=")[1]
        minuite = segment[6].split("_")[1]
        
        id = f"{student_id}-{year}/{month}/{day}/{hour}/{minuite}"
        data ={"id": id, "DetectedText": json.dumps(detected_text)}
        db_response = table.put_item(
           Item=data
        )
        id = student_id
        data ={"id": id, "DetectedText": json.dumps(detected_text)}
        db_response = table.put_item(
           Item=data
        )
        
        copy_source = {
            'Bucket': bucket,
            'Key': key,
            
        }
        s3.copy_object(CopySource=copy_source,Bucket=os.environ['StudentMarkingBucket'],Key=f"Screenshot/{student_id}.jpeg",ContentType='image/jpeg')

        print("PutItem and copy object succeeded!")
                
       
