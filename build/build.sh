#!/usr/bin/env bash

# build webapp container
docker build -t 192.168.42.100:5050/opal-webapp -f Dockerfile_webapp ..
docker push 192.168.42.100:5050/opal-webapp

# build database container
docker build -t 192.168.42.100:5050/opal-db -f Dockerfile_db .
docker push 192.168.42.100:5050/opal-db

kubectl apply -f yaml/app/
kubectl apply -f yaml/db/
kubectl apply -f yaml/nginx/