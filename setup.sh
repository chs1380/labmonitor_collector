npm uninstall -g aws-sam-local
sudo rm $(which sam)
sudo yum -y update
sudo yum -y install aws-cli
pip install --user aws-sam-cli
sudo -H pip install awscli --upgrade
alias sam=~/.local/bin/sam
sam --version
ln -sfn ~/.local/bin/sam ~/.c9/bin/sam
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
