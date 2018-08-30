import csv
import os
import hashlib
import boto3


cloudformation = boto3.client('cloudformation')
response = cloudformation.describe_stacks(
    StackName='labmonitor'
)

SEED = "Change it before generta API Key"
usageplanIds = next(x["OutputValue"] for x in response["Stacks"][0]["Outputs"] if x["OutputKey"] == "StudentPlan")

script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
rel_path = 'Source.csv'
abs_file_path = os.path.join(script_dir, 'Source.csv')
abs_out_file_path = os.path.join(script_dir, 'API_Keys.csv')

name_List = []
with open(abs_file_path) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        name_List.append(row)
        

with open(abs_out_file_path, 'w') as csvfile:
    fieldnames = ["Name","key","description","Enabled","usageplanIds"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for student in name_List:
        
        student["key"] = hashlib.sha224(student["ID"] + SEED).hexdigest()
        student["description"] = student["CLASS"] + "-" + student["NAME"]
        student["Name"] = student["ID"]
        student["Enabled"] = "TRUE"
        student["usageplanIds"] = usageplanIds
        del student["NAME"]
        del student["ID"]
        del student["CLASS"]
        writer.writerow(student)
        print(student)

apigateway = boto3.client('apigateway')
response = apigateway.import_api_keys(
    body=open(abs_out_file_path, 'r'),
    format='csv',
    failOnWarnings=True
)

print(response)
