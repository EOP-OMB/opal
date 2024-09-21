#!/usr/bin/env bash

# build webapp container
docker build -t registry2.omb.gov/security-apps/opal-webapp -f Dockerfile_webapp ..
docker push registry2.omb.gov/security-apps/opal-webapp


# build database container
docker build -t registry2.omb.gov/security-apps/opal-db -f Dockerfile_db .
docker push registry2.omb.gov/security-apps/opal-db

helm package ./opal/ --app-version $(cat ../version.txt)

#helm install opal opal-$(cat opal/Chart.yaml| grep version: | cut -d' ' -f2).tgz --atomic --create-namespace --debug
helm template opal opal-$(cat opal/Chart.yaml| grep version: | cut -d' ' -f2).tgz -f opal/stage_values.yaml > helm_output.yaml
echo "generated YAML file"
