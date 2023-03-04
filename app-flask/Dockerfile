FROM python:3.8-slim

EXPOSE 5001

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
## install Cmake to build dilb for face recognition 
### build-essential cmake pkg-config -> cmake

ARG HOST_UID

# RUN echo > /etc/apt/sources.list
# RUN echo  "deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bullseye main contrib non-free non-free-firmware" >/etc/apt/sources.list && \
#     echo  "deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bullseye-updates main contrib non-free non-free-firmware" >>/etc/apt/sources.list && \
#     echo  "deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bullseye-backports main contrib non-free non-free-firmware" >>/etc/apt/sources.list && \
#     echo  "deb https://mirrors.tuna.tsinghua.edu.cn/debian-security bullseye-security main contrib non-free non-free-firmware" >>/etc/apt/sources.list

# install dlib
# COPY ./dependents/dlib-19.24.0-cp38-cp38-linux_x86_64.whl .
# RUN python -m pip install ./dlib-19.24.0-cp38-cp38-linux_x86_64.whl && rm -rf ./dlib-19.24.0-cp38-cp38-linux_x86_64.whl

COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt  -i https://pypi.tuna.tsinghua.edu.cn/simple

# RUN wget http://www.ijg.org/files/jpegsrc.v8c.tar.gz && \
#     tar -zxvf jpegsrc.v8c.tar.gz && \
#     cd jpeg-8c/ &&\
#     export cc="gcc -arch i386" && \
#     ./configure && \
#     make && \
#     make install

# RUN export LD_LIBRARY_PATH=/usr/local/lib

# RUN apt-get update -y && \
#     apt-get install -y --no-install-recommends libx11-dev libgif-dev libpng-dev libxdmcp-dev && \
#     rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . /app

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser --disabled-password -u ${HOST_UID} appuser && chown -R appuser /app
USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD python run.py
