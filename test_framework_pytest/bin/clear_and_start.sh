#!/usr/bin/env bash

docker-compose down

#sudo rm -rf logs/*

ids='drs hds sql tests kafka confl zoo info'

for id in $ids
do
    echo 'id: '$id
    images=$(docker images | grep $id | awk '{print $3}')
    containers=$(docker container list | grep $id | awk '{print $1}')
    echo 'images: '$images
    echo 'containers: '$containers
    docker rmi $images --force
    docker rm $containers --force
done

sudo find . -name '.pytest_cache' -exec rm -rf {} \;
sudo find . -name '__pycache__' -exec rm -rf {} \;
sudo find . -name '__pycache__' -exec rm -rf {} \;

docker-compose up -d --build



