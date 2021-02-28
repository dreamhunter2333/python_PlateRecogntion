FROM  ubuntu:18.04
LABEL author=jinmu333

USER root

ENV LANG C.UTF-8
RUN sed -i s/archive.ubuntu.com/mirrors.aliyun.com/g /etc/apt/sources.list && \
    sed -i s/security.ubuntu.com/mirrors.aliyun.com/g /etc/apt/sources.list

RUN apt-get update -y && apt-get upgrade -y

RUN apt install python3-dev python3-pip -y
RUN apt-get install libzbar0 libsm6 libxrender1 libxext-dev -y
RUN apt-get update -y && apt-get upgrade -y

COPY ./docker/requirements.txt /opt/install/
RUN python3 -m pip install -r /opt/install/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

COPY ./flask_img /opt/flask_project/flask_img/
COPY ./start /opt/flask_project/
WORKDIR /opt/flask_project/

ENTRYPOINT ["python3", "/opt/flask_project/start"]
