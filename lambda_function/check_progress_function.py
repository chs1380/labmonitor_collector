import boto3
import json
import os
import datetime
from time import gmtime, strftime


print('Loading function')
s3 = boto3.client('s3')

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
    print(event)
    bucket = os.environ['StudentMarkingBucket']
    
    studentId = event['pathParameters']['studentId']
    lab =  event['pathParameters']['lab']
    lab = '{:02d}'.format(int(lab))
    prefix = f"{studentId}/lab{lab}"  
    
    get_filename = lambda key : os.path.split(key['Key'])[1]
    listing = list(map(lambda key: {'file': get_filename(key), 'time': key['LastModified'].strftime('%Y-%m-%d %H:%M:%S')}, 
                    s3.list_objects_v2(Bucket=bucket, Prefix=prefix)['Contents']))
    return respond(None, listing)