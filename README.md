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
3) inside the container terminal run - `service mongodb start` and then `mongo < setup_local_db.js`
4) create .env file with all configurations

Run appication:
1) run flask
