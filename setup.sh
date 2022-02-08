#!/bin/bash
pip install pytest pylint autopep8 rope
mkdir /root/.npm
mkdir /root/.npm/_logs
chmod -R 777 /root
pyright
redis-server --daemonize yes
service mongodb start
sleep 3
mongo < setup_local_db.js
