#!/bin/sh

#install Real-ESRGAN
git clone https://github.com/xinntao/Real-ESRGAN.git
cd Real-ESRGAN
pip install basicsr
pip install facexlib
pip install -r requirements.txt
python setup.py develop

cd ..  # back to the root dir.

#install the AWS cli
apt update
apt install curl
apt install unzip
apt install vim
apt install python3
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
./aws/install

#
#Copy over scripts for client work.
# We need Boto
pip3 install boto3
git clone https://github.com/davidbmar/4kUpScalerWorker.git
