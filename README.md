# Videos Backend

Setup Dev Env

Prepare IDE:
1) clone this repo
2) download and run vscode
3) install remove-containers extension

Install docker engine:
1) run - `sudo apt-get update`
2) run - `sudo apt-get install ca-certificates curl gnupg lsb-release`
3) run - `curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg`
4) run - `echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null`
5) run - `sudo apt-get update`
6) run - `sudo apt-get install docker-ce docker-ce-cli containerd.io`
7) run - `sudo usermod -aG docker $USER`
8) run - `sudo reboot`

Run conteiner:
1) open videos backend folder in vscode
2) cmd + p. than type `> Remote-Containers: Open folder in container`
3) create .env file with all configurations

Install and run local mongoDB:
1) run - `sudo apt-get install gnupg`
3) run - `wget -qO - https://www.mongodb.org/static/pgp/server-5.0.asc | sudo apt-key add -`
4) run - `lsb_release -dc`
5) run - `echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/5.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-5.0.list`
6) run - `sudo apt-get update`
7) run - `sudo apt-get install -y mongodb-org`
8) run - `sudo systemctl start mongod` or `sudo service mongod restart`
9) run - `mongo`
10) run - `use videos`
11) run - `db.createUser({user: "root", pwd:  "root", roles: [ { role: "readWrite", db: "videos" }]})`
12) update `.env` file with the db configuration

Install ngrok
1) run - `sudo apt update`
2) run - `sudo apt install snapd`
3) run - `snap install ngrok`
4) register to ngrok and get token
5) run - `ngrok tcp 27017`
6) in `.env` file update `MONGO_HOST` variable to be `mongodb://{ngrok_url}/{db_name}`

Run appication:
1) run flask
