#!/usr/bin/env bash

# build webapp container
docker build -t 192.168.42.100:5050/opal-webapp -f Dockerfile_webapp ..
docker push 192.168.42.100:5050/opal-webapp

# build database container
docker build -t 192.168.42.100:5050/opal-db -f Dockerfile_db .
docker push 192.168.42.100:5050/opal-db

helm package ./opal/ --app-version $(cat ../version.txt)

#helm install opal opal-$(cat opal/Chart.yaml| grep version: | cut -d' ' -f2).tgz --atomic --create-namespace --debug
helm template opal opal-$(cat opal/Chart.yaml| grep version: | cut -d' ' -f2).tgz > helm_output.yaml
