#!/bin/bash

# This uses natural forign keys, but that doesn't work
#python /opt/opal/manage.py dumpdata -a --indent 2 --format json --natural-foreign --natural-primary -o "/opt/opal/ssp/fixtures/prod_data/$(date +"%Y_%m_%d_%I_%M_%p")_omb_data.json" -v3

python /opt/opal/manage.py dumpdata -a --indent 2 --format json -o "/opt/opal/ssp/fixtures/prod_data/$(date +"%Y_%m_%d_%I_%M_%p")_omb_data.json" -v3

git add "/opt/opal/ssp/fixtures/prod_data/$(date +"%Y_%m_%d_%I_%M_%p")_omb_data.json"
git commit -m "New data Dump"
git push
