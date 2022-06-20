FROM ubuntu:20.04
ENV DEBIAN_FRONTEND=noninteractive
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8
RUN apt-get update -y && apt-get install -y python3-pip python3-venv apt-utils libspatialindex-dev --no-install-recommends
RUN python3 -m venv $VIRTUAL_ENV
RUN useradd --create-home appuser
WORKDIR /appuser
RUN chown -R appuser:appuser /opt/venv /appuser /home/appuser
COPY requirements.txt .
RUN pip install wheel
RUN pip --no-cache-dir install -r requirements.txt
RUN apt-get clean && apt-get autoclean && apt-get autoremove -y && rm -rf /var/lib/cache/* && rm -rf /var/lib/log/*
RUN apt-get update && apt-get install -y zsh git nano wget --no-install-recommends
RUN apt-get clean && apt-get autoclean && apt-get autoremove -y && rm -rf /var/lib/cache/* && rm -rf /var/lib/log/*
EXPOSE 5555
EXPOSE 8000
ARG GITVER
ENV GITVER ${GITVER}
RUN chown -R appuser:appuser /opt/venv /appuser /home/appuser

RUN apt-get -y update
RUN apt-get install -y redis-server
RUN apt-get install -y ffmpeg

COPY setup.sh .
COPY setup_mysql.sh .
RUN apt-get -y update
RUN apt-get install -y mariadb-server
RUN chmod 777 ./setup.sh
EXPOSE 3306
EXPOSE 6379
RUN git config --global --add safe.directory /workspaces/videos_backend
