import boto3
import json
import os
import tarfile,sys,shutil


print('Loading function')
s3 = boto3.client('s3')
apigateway = boto3.client('apigateway')

def lambda_handler(event, context):
    dirpath = os.getcwd()
    print("current directory is : " + dirpath)
    apiKey = apigateway.get_api_key(apiKey=event["requestContext"]["identity"]["apiKeyId"],includeValue=True)
    
    body = json.loads(event["body"])
    print(type(body))
    print(body)
    s3.put_object(Bucket=os.environ['StudentLabDataBucket'], Key="code/"+ apiKey["name"] + body["key"],
              Body=body["code"],
              Metadata={"ip":event["requestContext"]["identity"]["sourceIp"], },
              ContentType="application/json"
          )
          
    print(apiKey)
    setup_git()
    clone_source()
    overwrite_source_code(body)
    test_result = run_unit_test(body, dirpath)
    print(test_result)
    return respond(None, {"test_result": test_result})


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
    
    shutil.copyfile("git-2.4.3.tar", os.path.join(targetDirectory, "git-2.4.3.tar"))
    os.chdir(targetDirectory)
    untar(os.path.join(targetDirectory, "git-2.4.3.tar"))
    os.system('git --version')
    
    
def clone_source():
    os.chdir("/tmp/")
    if os.path.isdir("/tmp/ite3101_introduction_to_programming"):
        shutil.rmtree("/tmp/ite3101_introduction_to_programming")
    os.system('git clone -b server https://github.com/wongcyrus/ite3101_introduction_to_programming.git')
    
    
def overwrite_source_code(body):
    code_file_path = "/tmp/ite3101_introduction_to_programming/lab/" + body["key"]
    os.remove(code_file_path)
    with open(code_file_path, "w+") as codefile:
        codefile.write(body["code"])
    os.system("cat " + code_file_path)
    
def run_unit_test(body, dirpath):
    segment = body["key"].split("/")
    os.environ['PATH'] = os.environ['PATH'] + ":" +  os.environ['LAMBDA_RUNTIME_DIR']
    os.chdir(dirpath)
    return os.popen('python pytest.py /tmp/ite3101_introduction_to_programming/tests/' + segment[1] + "/test_"+ segment[2]).read()
            
            
def respond(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
        },
    }


