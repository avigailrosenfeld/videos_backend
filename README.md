# Videos Backend

Setup Dev Env

Prepare IDE:
1) clone this repo
2) download vscode
3) install remove-containers extension

Install docker engine:
1) run - `sudo apt-get install ca-certificates curl gnupg lsb-release`
2) run - `curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg`
3) run - `echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null`
4) run - `sudo apt-get update`
5) run - `sudo apt-get install docker-ce docker-ce-cli containerd.io`

Run conteiner:
1) open videos backend folder in vscode
2) cmd + p. than type `> Remote-Containers: Open folder in container`
3) cmd + p. than type `> select interpreter`, and select - `Use python from 'python.defaultInerpreterPath' setting`

Run appication:
1) run flask

Install and run local mongoDB:
1) install
2) run
3) create new db
4) update `.env` file

Install ngrok
1) install
2) create account
3) run - `ngrok tcp 27017`
4) in `.env` file update MONGO_HOST variable to be `mongodb://{ngrok_url}/{db_name}
