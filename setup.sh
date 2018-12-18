sudo yum -y update
sudo yum -y install aws-cli
sudo -H pip install awscli --upgrade
pip install --user aws-sam-cli -U
sam --version
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
