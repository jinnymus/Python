#!/usr/bin/env bash

container=$1
echo 'container: '$container
container_id=`docker ps -a | grep $container | awk '{print $1}'`
image_id=`docker images | grep $container | awk '{print $3}'`
echo 'container_id: '$container_id
echo 'image_id: '$image_id
echo 'stopping container...'
docker stop $container_id
echo 'delete container...'
docker rm $container_id
echo 'delete image...'
docker rmi -f $image_id
echo 'start container...'
docker-compose up -d $container
