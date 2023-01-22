if [ $(docker images | grep "none" | awk '{print $3}' | head -1) ] ; then
    docker rmi $(docker images | grep "none" | awk '{print $3}')
fi
echo "docker compose start."
export MYUID=1001
docker compose up -d --build