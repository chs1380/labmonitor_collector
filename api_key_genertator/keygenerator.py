import csv
import os
import hashlib
import boto3



SEED = "Change it before generta API Key a"
usageplanIds = "805wyk"

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
        student["description"] = student["NAME"]
        student["Name"] = student["ID"]
        student["Enabled"] = "TRUE"
        student["usageplanIds"] = usageplanIds
        del student["NAME"]
        del student["ID"]
        writer.writerow(student)
        print(student)

apigateway = boto3.client('apigateway')
response = apigateway.import_api_keys(
    body=open(abs_out_file_path, 'r'),
    format='csv',
    failOnWarnings=True
)

print(response)