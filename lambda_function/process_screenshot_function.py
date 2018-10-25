import boto3
import os
import sys
import uuid
import urllib.parse
import json
from PIL import Image
import PIL.Image

rekognition_client = boto3.client('rekognition', region_name='us-east-1')
dynamodb = boto3.resource('dynamodb')
s3 = boto3.client('s3')

def top(image_path, saved_location):
    with Image.open(image_path) as image_obj:
        width, height = image_obj.size
        cropped_image = image_obj.crop((width - 200, 0, width, 200))
        cropped_image.save(saved_location)

    
def lambda_handler(event, context):
    db = os.environ['ScreenshotMetaDataTable']
    table = dynamodb.Table(os.environ['ScreenshotMetaDataTable'])
    
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']

        download_path = '/tmp/{}.jpeg'.format(uuid.uuid4())
        
        key = urllib.parse.unquote(key)
        s3.download_file(bucket, key, download_path)
        
        top(download_path, '/tmp/cropped.jpg')
        
        with open('/tmp/cropped.jpg', 'rb') as image:
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
            'Key': key
        }
    
        s3.copy_object( CopySource=copy_source,
                        Bucket=os.environ['StudentMarkingBucket'],
                        Key=f"Screenshot/{student_id}.jpeg",
                        MetadataDirective='REPLACE',
                        ContentType='image/jpeg')

        print("PutItem and copy object succeeded!")
                
       
