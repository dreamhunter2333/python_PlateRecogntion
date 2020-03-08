#!bin/bash
apt-get update -y && apt-get upgrade -y
apt install python3-dev python3-pip -y
apt-get install libzbar0 libxext-dev libsm6 libxrender1 -y
apt-get update -y && apt-get upgrade -y
cd /opt/flask_project
python3 -m pip install -r docker/requirements.txt
pytest