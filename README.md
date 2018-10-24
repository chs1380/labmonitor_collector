# labmonitor_collector

## Cloud 9 Setup ##

git clone https://github.com/wongcyrus/labmonitor_collector.git  
cd labmonitor_collector/  
chmod +x *.sh  
./setup.sh  


after that you may need to run  
source venv/bin/activate  
if you found that you are not under the Python 3 Virtual Environment.


You need to set environment variable STACK_NAME before you run the deployment.sh.
To generate API for your class, you need to update Source.csv and run python api_key_genertator/keygenerator.py
To delete all API Key for your stack, python api_key_genertator/delete_key.py
Delete stack with cleanup.sh.

