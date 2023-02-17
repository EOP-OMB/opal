#!/usr/bin/env bash

#VER_NUM=$(git describe --tags --always | cut -d "-" -f3)
VER_NUM=$(semver -i patch $(cat version.txt))
echo $VER_NUM > version.txt
REGISTRY=registry2.omb.gov/security-apps

docker build -t $REGISTRY/opal:$VER_NUM ../../.
docker push $REGISTRY/opal:$VER_NUM
kubectl set image deployment/opal opal=$REGISTRY/opal:$VER_NUM
