#!/bin/bash
pip install pytest pylint autopep8 rope
service mongodb start
sleep 3
mongo < setup_local_db.js
chmod -R 777 /root/.npm