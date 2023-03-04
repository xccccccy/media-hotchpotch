# media-hotchpotch
Something about Imitation media, include book, video and music etc.

# install docker
sudo yum install yum-utils
sudo yum-config-manager --add-repo http://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo
sudo yum -y update
sudo yum install docker-ce docker-ce-cli containerd.io docker-compose-plugin


# useradd xcy
# passwd wd
# xcy   ALL=(ALL) ALL
# :w !sudo tee %

# wget https://mirrors.tuna.tsinghua.edu.cn/anaconda/archive/Anaconda3-2021.05-Linux-x86_64.sh

## tuna anaconda mirrors
# channels:
#   - defaults
# show_channel_urls: true
# default_channels:
#   - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main
#   - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/r
#   - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/msys2
# custom_channels:
#   conda-forge: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
#   msys2: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
#   bioconda: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
#   menpo: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
#   pytorch: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
#   pytorch-lts: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
#   simpleitk: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud

# # not need # conda env export | grep -v "^prefix: " > environment.yml
# conda env create -f environment.yml

# wget https://github.com/coder/code-server/releases/download/v4.0.2/code-server-4.0.2-linux-amd64.tar.gz
# tar -xzvf code-server-4.0.2-linux-amd64.tar.gz
# vim ~/.config/code-server/config.yaml 
# ./code-server 

# sudo yum -y install rsync

# sudo yum install nginx
# sudo vim /etc/nginx/nginx.conf

# 配置ssl
# sudo cp -vr ~/flaskProject/ssl/ /etc/nginx/
# sudo nginx -s reload

# github action del
echo ${SSL_KEY} > nginx/xcya.key && echo ${SSL_PEM} > nginx/xcya.pem

# open face recognize
dlib==19.24.0
face-recognition==1.3.0
opencv-contrib-python-headless<=4.2
Pillow==9.4.0