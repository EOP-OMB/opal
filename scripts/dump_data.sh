#!/bin/bash
python /opt/opal/manage.py dumpdata -a --indent 2 --format json --natural-foreign --natural-primary -o "/opt/opal/ssp/fixtures/prod_data/$(date +"%Y_%m_%d_%I_%M_%p")_omb_data.json" -v3
