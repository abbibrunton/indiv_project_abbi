cd ..
sudo apt-get -y install python3-venv
sudo apt-get -y install virtualenv
sudo pip3 install -r requirements.txt
cd application
. venv/bin/activate
cd ..
python3 run.py
