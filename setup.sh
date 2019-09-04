# Change to default Python3
sudo mv /usr/bin/python /usr/bin/python2
sudo ln -s /usr/bin/python3 /usr/bin/python
python --version
# Install Code Formatter for Python and you need to set AWS Cloud9「Preferences」->「Python Support」->「Custom Code Formatter」
# yapf -i "$file"
sudo pip install yapf
sudo yum -y update
sudo yum -y install aws-cli
sudo -H pip install awscli --upgrade
# Install brew and update SAM CLI to the latest version.
yes | sh -c "$(curl -fsSL https://raw.githubusercontent.com/Linuxbrew/install/master/install.sh)"
test -d ~/.linuxbrew && eval $(~/.linuxbrew/bin/brew shellenv)
test -d /home/linuxbrew/.linuxbrew && eval $(/home/linuxbrew/.linuxbrew/bin/brew shellenv)
test -r ~/.bash_profile && echo "eval \$($(brew --prefix)/bin/brew shellenv)" >>~/.bash_profile
echo "eval \$($(brew --prefix)/bin/brew shellenv)" >>~/.profile
brew --version
brew tap aws/tap
brew install aws-sam-cli
sam --version
