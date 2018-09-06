#!/usr/bin/env bash

sudo find . -name '.pytest_cache' -exec rm -rf {} \;
sudo find . -name '__pycache__' -exec rm -rf {} \;
sudo find . -name '__pycache__' -exec rm -rf {} \;
sudo find . -name 'nistest.egg-info' -exec rm -rf {} \;
sudo rm -rf pytest/report
sudo rm -rf pytest/allure
sudo rm -rf *.deb
sudo rm -rf nis-test-version

id='stubs'

echo 'id: '$id
images=$(docker images | grep $id | awk '{print $3}')
containers=$(docker container list | grep $id | awk '{print $1}')
echo 'images: '$images
echo 'containers: '$containers
docker kill $containers
docker rmi $images --force
docker rm $containers --force

docker-compose -f docker-compose_stubs.yml up --build -d
im=$(docker images | grep $id | awk '{print $3}')
echo 'im: '$im
docker tag $im repo.nis-glonass.ru/nis-test/stubs:latest
docker push repo.nis-glonass.ru/nis-test/stubs:latest

docker-compose -f docker-compose_stubs.yml down

