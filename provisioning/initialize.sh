#!/bin/bash

# WARNING: This script has not been tested. It is currently serving as documentation than an actual automated script

apt-get update
apt-get upgrade

apt-get install fail2ban

useradd -r -m -s /bin/bash deploy

# Python
apt-get install -y python-setuptools
easy_install -U pip
pip install virtualenv

apt-get install -y git
# HERE WE SET DEPLOY'S SSH KEYS

cd /home/deploy
git clone git@github.com:justiniso/retailbase.git

