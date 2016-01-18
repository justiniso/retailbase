#!/bin/bash

# WARNING: This script has not been tested. It is currently serving as documentation than an actual automated script

apt-get update
apt-get upgrade

apt-get install fail2ban

useradd -r -m -s /bin/bash deploy

chmod 777 /var/log

# Python
apt-get install -y python-setuptools
easy_install -U pip
pip install virtualenv

apt-get install -y git
# HERE WE SET DEPLOY'S SSH KEYS

cd /home/deploy
git clone git@github.com:justiniso/retailbase.git

apt-add-repository ppa:nginx/stable
apt-get update
apt-get install -y nginx
ln -nsf /home/deploy/retailbase/provisioning/etc/nginx/conf.d/app.conf /etc/nginx/conf.d/app.conf

# COMMENT OUT THE LINE IN nginx.conf THAT SAYS include /etc/nginx/sites-enabled/*;


apt-get install -y mongodb
mongod

cd /home/deploy
gunicorn -D -b 0.0.0.0:8000 application:application