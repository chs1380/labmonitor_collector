import csv
import os
import boto3

stackname='testmonitor'

script_dir = os.path.dirname(__file__) 
rel_path = 'Source.csv'
abs_file_path = os.path.join(script_dir, 'Source.csv')

name_dict = {}
with open(abs_file_path) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        name_dict[row["ID"]+ "_" +stackname] = row["NAME"] 
        
apigateway = boto3.client('apigateway')

response = apigateway.get_api_keys(
    limit=500,
    includeValues=True
)

for item in response["items"]:
    if item["name"] in name_dict:
        print(item)
        response = apigateway.delete_api_key(
            apiKey=item["id"]
        )
        print(response)

