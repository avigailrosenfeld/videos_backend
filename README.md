# Videos Backend

Setup Dev Env

Prepare IDE:
1) clone this repo
2) download and run vscode - https://code.visualstudio.com/download
3) install docker engine - https://docs.docker.com/engine/install/ubuntu/
4) install remote-containers extension in vscode

Run Conteiner:
1) open videos_backend folder in vscode
2) cmd + p. than type `> Remote-Containers: Open folder in container`

Run Appication:
1) run flask
2) run celery worker

Monitor Celery Workers:
1) run celery flower
2) open `http://localhost:5555` in your browser 

Run API Tests:
1) run flask test
2) run API tests

Run Pyright:
1) run - `pyright`

Run Mypy:
1) run - `mypy`
