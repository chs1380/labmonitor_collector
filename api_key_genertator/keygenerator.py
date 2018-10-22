import csv
import os
import hashlib
import boto3

stackname='testmonitor'

cloudformation = boto3.client('cloudformation')
response = cloudformation.describe_stacks(
    StackName=stackname
)

usageplan_ids = next(x["OutputValue"] for x in response["Stacks"][0]["Outputs"] if x["OutputKey"] == "StudentPlan")
lab_collector_api = next(x["OutputValue"] for x in response["Stacks"][0]["Outputs"] if x["OutputKey"] == "LabCollectorApi")

print("api\t\t"+lab_collector_api)
print("usageplan_ids\t"+usageplan_ids)

SEED = usageplan_ids #This ensure the it will not be the same for each stack.

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
    fieldnames = ["Name","key","description","Enabled","usageplan_ids"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for student in name_List:
        key_material = (student["ID"] + SEED).encode('utf-8')
        student["key"] = hashlib.sha224(key_material).hexdigest()
        student["description"] =  student["CLASS"] + "-" + student["NAME"]
        student["Name"] = student["ID"] + "_" +stackname
        student["Enabled"] = "TRUE"
        student["usageplan_ids"] = usageplan_ids
        del student["NAME"]
        del student["ID"]
        del student["CLASS"]
        writer.writerow(student)

apigateway = boto3.client('apigateway')
response = apigateway.import_api_keys(
    body=open(abs_out_file_path, 'r'),
    format='csv',
    failOnWarnings=True
)

print(response["ids"])

for api_key_id in response["ids"]:
    response = apigateway.create_usage_plan_key(
        usagePlanId=usageplan_ids,
        keyId=api_key_id,
        keyType='API_KEY'
    )
    print(response)