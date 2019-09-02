import sys
sys.path.append("/opt/")
import boto3
import json
import os
import subprocess
import tarfile,shutil

print('Loading function')
s3 = boto3.client('s3')
apigateway = boto3.client('apigateway')

SOURCE_RESPOSITORY_NAME = os.environ['SourceRespositoryName']

def lambda_handler(event, context):
    dirpath = os.getcwd()
    print("current directory is : " + dirpath)
    apiKey = apigateway.get_api_key(apiKey=event["requestContext"]["identity"]["apiKeyId"],includeValue=True)
    
    body = json.loads(event["body"])
    key = get_key(body)
    student_id = apiKey["name"].split("_")[0]
    s3.put_object(Bucket=os.environ['StudentLabDataBucket'], Key="code/"+ student_id + key,
                  Body=body["code"],
                  Metadata={"ip":event["requestContext"]["identity"]["sourceIp"], },
                  ContentType="application/json"
                )
          
    print(apiKey)
    
    if not str_to_bool(os.environ['RunUnitTest']):
        return respond(None, {"test_result": "Run unittest is disabled."})
        
    setup_git()
    clone_source()
    overwrite_source_code(body)
    test_result = run_unit_test(body)
    print(test_result)
    print(test_result.splitlines())
    is_pass_all_tests = "FAILED" not in test_result
 
    s3.put_object(Bucket=os.environ['StudentLabDataBucket'], Key="test_result/"+ student_id + key,
                  Body=test_result,
                  Metadata={"ip":event["requestContext"]["identity"]["sourceIp"], },
                  ContentType="text/plain"
            )
            
    if is_pass_all_tests:
        s3.put_object(Bucket=os.environ['StudentMarkingBucket'], Key=""+ student_id + key,
              Body=test_result,
              Metadata={"ip":event["requestContext"]["identity"]["sourceIp"], },
              ACL='public-read',
              ContentType="text/plain"
        )

    return respond(None, {"test_result": test_result + "\n" + str(is_pass_all_tests)})


def get_key(body):
    return body["key"].replace("\\","/")
    

def str_to_bool(s):
    if s == 'true':
         return True
    elif s == 'false':
         return False
    else:
         raise ValueError
         
         
def untar(fname):
    if (fname.endswith("tar")):
        tar = tarfile.open(fname)
        tar.extractall()
        tar.close()
        print("Extracted in Current Directory")
    else:
        print("Not a tar file: '%s '" % sys.argv[0])


def setup_git():
    targetDirectory = "/tmp/git/"
    GIT_TEMPLATE_DIR = os.path.join(targetDirectory, 'usr/share/git-core/templates');
    GIT_EXEC_PATH = os.path.join(targetDirectory, 'usr/libexec/git-core');
    LD_LIBRARY_PATH = os.path.join(targetDirectory, 'usr/lib64');
    binPath = os.path.join(targetDirectory, 'usr/bin');
    
    os.environ['GIT_TEMPLATE_DIR'] = GIT_TEMPLATE_DIR
    os.environ['GIT_EXEC_PATH'] = GIT_EXEC_PATH
    os.environ['LD_LIBRARY_PATH'] =   os.environ['LD_LIBRARY_PATH'] + ":" + LD_LIBRARY_PATH if os.environ['LD_LIBRARY_PATH'] else LD_LIBRARY_PATH;
    os.environ['PATH'] = os.environ['PATH'] + ":" + binPath
    
    if os.path.isdir("/tmp/git/"):
        return
    os.makedirs(targetDirectory)
    
    shutil.copyfile("/opt/git-2.4.3.tar", os.path.join(targetDirectory, "git-2.4.3.tar"))
    os.chdir(targetDirectory)
    untar(os.path.join(targetDirectory, "git-2.4.3.tar"))
    os.system('git --version')
    
    
def clone_source():
    os.chdir("/tmp/")
    if os.path.isdir(f"/tmp/{SOURCE_RESPOSITORY_NAME}"):
        shutil.rmtree(f"/tmp/{SOURCE_RESPOSITORY_NAME}")
    os.system(os.environ['GitCommand'])
    
    
def overwrite_source_code(body):
    code_file_path = f"/tmp/{SOURCE_RESPOSITORY_NAME}/lab/" + get_key(body)
    os.remove(code_file_path)
    with open(code_file_path, "w+") as codefile:
        codefile.write(body["code"])

def run_unit_test(body):
    segment = get_key(body).split("/")
    os.environ['PATH'] = os.environ['PATH'] + ":" +  os.environ['LAMBDA_RUNTIME_DIR']
    os.chdir(f"/tmp/{SOURCE_RESPOSITORY_NAME}")
    print(f'python -m unittest tests/' + segment[1] + "/test_"+ segment[2])
    return subprocess.getoutput(f'python -m unittest tests/' + segment[1] + "/test_"+ segment[2])
            
            
def respond(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
        },
    }


