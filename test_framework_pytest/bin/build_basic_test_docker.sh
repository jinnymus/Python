#!/usr/bin/env bash

python_version=$1

sudo find . -name '.pytest_cache' -exec rm -rf {} \;
sudo find . -name '__pycache__' -exec rm -rf {} \;
sudo find . -name '__pycache__' -exec rm -rf {} \;
sudo find . -name 'nistest.egg-info' -exec rm -rf {} \;
sudo rm -rf pytest/report
sudo rm -rf pytest/allure
sudo rm -rf *.deb
sudo rm -rf nis-test-version

ids='<none> tests basic_test basic_test tests'

for id in $ids
do
    echo 'id: '$id
    echo 'python_version: '$python_version
    #images=$(docker images | grep $id | grep python$python_version | awk '{print $3}')
    #containers=$(docker container list | grep $id | grep python$python_version | awk '{print $1}')
    images=$(docker images | grep $id | awk '{print $3}')
    containers=$(docker container list | grep $id | awk '{print $1}')
    echo 'images: '$images
    echo 'containers: '$containers
    docker kill $containers
    docker rmi -f $images --force
    docker rm $containers --force
done

id='basic_test'

docker-compose -f docker-compose_basic_test_python$python_version.yml up --build -d --remove-orphans
im=$(docker images | grep $id | awk '{print $3}')
echo 'im: '$im
docker tag $im repo.nis-glonass.ru/base_images/basic_test:python$python_version
docker push repo.nis-glonass.ru/base_images/basic_test:python$python_version

docker-compose -f docker-compose_basic_test_python$python_version.yml down

