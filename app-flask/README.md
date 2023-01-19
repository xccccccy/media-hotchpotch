# flask-vue-myworld
flask+vue3+vite

# environment
flask
flask_cors
sqlite

## environment install
conda create -n flask python=3.8
pip install flask flask_cors flask_mail opencv-python requests bs4 lxml tqdm flask_sqlalchemy
# macos
 brew install cmake
# linux
 see below
pip install face_recognition

## environment install with pipenv
pip3 install pipenv
pipenv --python 3.8
pipenv install flask flask_cors flask_mail opencv-python requests bs4 lxml tqdm flask_sqlalchemy
# need cmake
pipenv install face_recognition

## cmake install
# macos
1、 brew install cmake
2、 wget https://github.com/Kitware/CMake/releases/download/v3.25.1/cmake-3.25.1-macos-universal.tar.gz
    tar -zxvf cmake-3.25.1-macos-universal.tar.gz
    cd cmake-3.25.1-macos-universal/biin
    cmake -version
    sudo ln -s cmake /usr/bin/cmake
# linux
1、 sudo apt install cmake
2、 sudo yum install -y cmake
3、 wget https://github.com/Kitware/CMake/releases/download/v3.25.1/cmake-3.25.1-linux-x86_64.tar.gz
    tar -zxvf cmake-3.25.1-linux-x86_64.tar.gz
    cd cmake-3.25.1-linux-x86_64/biin
    cmake -version
    sudo ln -s cmake /usr/bin/cmake


