import boto3
import os
import boto3
from botocore.exceptions import ClientError
from os import environ

rekognition=boto3.client('rekognition', region_name='us-east-1')
collectionId='AwsFaceCollection'
image_bucket="awshackathonsumerian-s3bucket-4lfa7pkflhlz"
prefix = "face/"

def delete_collection():
    print('Attempting to delete collection ' + collectionId)
    statusCode=''
    try:
        response=rekognition.delete_collection(CollectionId=collectionId)
        statusCode=response['StatusCode']
        
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            print ('The collection ' + collectionId + ' was not found ')
        else:
            print ('Error other than Not Found occurred: ' + e.response['Error']['Message'])
        statusCode=e.response['ResponseMetadata']['HTTPStatusCode']
    print('Operation returned Status Code: ' + str(statusCode))
    print('Done...')


def create_collection():
    maxResults=2
    #Create a collection
    print('Creating collection:' + collectionId)
    response=rekognition.create_collection(CollectionId=collectionId)
    print('Collection ARN: ' + response['CollectionArn'])
    print('Status code: ' + str(response['StatusCode']))
    print('Done...')

def index_face():
    s3 = boto3.client('s3')  # again assumes boto.cfg setup, assume AWS S3
    for key in s3.list_objects_v2(Bucket=image_bucket, Prefix=prefix)['Contents']:
        path, filename = os.path.split(key['Key'])
        filename = filename.replace(" ", "_")
        filename, ext = os.path.splitext(filename)
        if filename == "":
            continue
        response=rekognition.index_faces(CollectionId=collectionId,
                                    Image={'S3Object':{'Bucket':image_bucket,'Name':key['Key']}},
                                    ExternalImageId=filename,
                                    DetectionAttributes=['ALL'])
        print ('Faces in ' + filename) 							
        for faceRecord in response['FaceRecords']:
             print (faceRecord['Face']['FaceId'])


if __name__ == "__main__":
    delete_collection()
    create_collection()
    index_face()