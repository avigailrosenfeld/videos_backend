# videos_backend

Setup Dev Env

prepare IDE:
1) clone this repo
2) download vscode
3) install remove-containers extension

install docker engine:
1) run - sudo apt-get install ca-certificates curl gnupg lsb-release
2) run - curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
3)  echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
4) run - sudo apt-get update
5) run - sudo apt-get install docker-ce docker-ce-cli containerd.io



