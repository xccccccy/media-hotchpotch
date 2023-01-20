if [ $(docker images | grep "none" | awk '{print $3}') ] ; then
    docker rmi $(docker images | grep "none" | awk '{print $3}')
fi

docker compose up -d --build