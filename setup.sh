#!/bin/bash
pip install pytest pylint autopep8 rope
mkdir /root/.npm
mkdir /root/.npm/_logs
chmod -R 777 /root
pyright
redis-server --daemonize yes
service mysql start
bash ./setup_mysql.sh

