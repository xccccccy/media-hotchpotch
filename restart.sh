if [ $(docker images | grep "none" | awk '{print $3}') ] ; then
    docker rmi $(docker images | grep "none" | awk '{print $3}')
fi
echo "compose start."
docker compose up -d --build