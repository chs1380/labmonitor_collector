import boto3
from time import gmtime, strftime
import os

s3 = boto3.client('s3')
studentId = "180066119"
lab =  "1"
lab = '{:02d}'.format(int(lab))
prefix = f"{studentId}/lab{lab}" 
bucket = "labmonitor-studentmarkingbucket-ed0gzeqsp47l"

client = boto3.client('s3')
get_filename = lambda key : os.path.split(key['Key'])
listing = list(map(lambda key: {'file': get_filename(key), 'time': key['LastModified'].strftime('%Y-%m-%d %H:%M:%S')}, 
                                s3.list_objects_v2(Bucket=bucket, Prefix=prefix)['Contents']))
print(listing)