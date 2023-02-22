#!/usr/bin/env bash

#VER_NUM=$(git describe --tags --always | cut -d "-" -f3)
echo $(semver -i patch $(cat version.txt)) > version.txt
REGISTRY=registry2.omb.gov/security-apps

docker build -t $REGISTRY/opal:$(cat version.txt) ../../.
docker push $REGISTRY/opal:$(cat version.txt)
kubectl set image deployment/opal opal=$REGISTRY/opal:$(cat version.txt)



