sudo pip install yapf
sudo rm $(which sam)
pip install --user aws-sam-cli
sam --version
ln -sfn $(which sam) ~/.c9/bin/sam
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
