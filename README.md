# labmonitor_collector

## Cloud 9 Setup ##


1. Get Source Code and update the Cloud 9 Environment.
git clone https://github.com/wongcyrus/labmonitor_collector.git  
cd labmonitor_collector/  
chmod +x *.sh  
./setup.sh  


2. Change region (Optional) and run
. ./setup_config.sh

3. Prepare Lambda Layer
./get_layer_packages.sh

4. Deploy Application
./deployment.sh

You need to set environment variable STACK_NAME before you run the deployment.sh.
To generate API for your class, you need to update Source.csv and run python api_key_genertator/keygenerator.py
To delete all API Key for your stack, python api_key_genertator/delete_key.py
Delete stack with cleanup.sh.

