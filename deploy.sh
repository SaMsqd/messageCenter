#!/bin/bash
echo "Stop container"
docker stop message-center
docker rm frontend
docker image rm samsqd/message-center
echo "Pull image"
docker pull samsqd/message-center
echo "Start container"
docker run -p 8000:80 --name message-center -e URL=http://185.41.160.212/ -t samsqd/message-center
echo "Finish deploying!"