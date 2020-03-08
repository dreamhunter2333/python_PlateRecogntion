FROM  ubuntu:latest
LABEL author=jinmu333

USER root

ENV LANG C.UTF-8
RUN sed -i s/archive.ubuntu.com/mirrors.aliyun.com/g /etc/apt/sources.list && \
    sed -i s/security.ubuntu.com/mirrors.aliyun.com/g /etc/apt/sources.list

RUN apt-get update -y && apt-get upgrade -y

RUN apt-get install sudo curl zsh wget nano psmisc -y
RUN apt-get update -y && apt-get upgrade -y
RUN apt-get install screenfetch git -y
RUN apt install python3-dev python3-pip -y
ENV SHELL=/bin/zsh
RUN git clone git://github.com/robbyrussell/oh-my-zsh.git ~/.oh-my-zsh && \
    cp ~/.oh-my-zsh/templates/zshrc.zsh-template ~/.zshrc

RUN python3 -m pip install autopep8 pylint -i https://pypi.tuna.tsinghua.edu.cn/simple
COPY ./requirements.txt /opt/install/
RUN python3 -m pip install -r /opt/install/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN apt-get update -y && apt-get upgrade -y
RUN apt-get install libzbar0 libsm6 libxrender1 -y
RUN apt-get update -y && apt-get upgrade -y
RUN rm -rf /root/.cache/ /opt/install
ENTRYPOINT ["python3", "/opt/flask_project/start"]

WORKDIR /opt/flask_project/
