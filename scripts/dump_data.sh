#!/bin/bash
python manage.py dumpdata ssp --indent 2 > "/opt/opal/ssp/fixtures/prod_data/$(date +"%Y_%m_%d_%I_%M_%p")_omb_data.log"
