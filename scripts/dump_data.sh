#!/bin/bash

# This uses natural forign keys, but that doesn't work
#python /opt/opal/manage.py dumpdata -a --indent 2 --format json --natural-foreign --natural-primary -o "/opt/opal/ssp/fixtures/prod_data/$(date +"%Y_%m_%d_%I_%M_%p")_omb_data.json" -v3

#!/bin/bash

python /opt/opal/manage.py dumpdata ssp.status -o /opt/opal/ssp/fixtures/fixture_status.json --indent 2
python /opt/opal/manage.py dumpdata ssp.information_type -o /opt/opal/ssp/fixtures/fixture_information_type.json --indent 2
python /opt/opal/manage.py dumpdata ssp.user_function -o /opt/opal/ssp/fixtures/fixture_user_function.json --indent 2
python /opt/opal/manage.py dumpdata ssp.user_privilege -o /opt/opal/ssp/fixtures/fixture_user_privilege.json --indent 2
python /opt/opal/manage.py dumpdata ssp.user_role -o /opt/opal/ssp/fixtures/fixture_user_role.json --indent 2
python /opt/opal/manage.py dumpdata ssp.port_range ssp.protocol -o /opt/opal/ssp/fixtures/fixture_protocal_and_port.json --indent 2
python /opt/opal/manage.py dumpdata ssp.inventory_item_type -o /opt/opal/ssp/fixtures/inventory_item_type.json --indent 2

python /opt/opal/manage.py dumpdata -a --indent 2 --format json -o "/opt/opal/ssp/fixtures/prod_data/$(date +"%Y_%m_%d_%I_%M_%p")_omb_data.json" -v3

git add "/opt/opal/ssp/fixtures/prod_data/$(date +"%Y_%m_%d_%I_%M_%p")_omb_data.json"
git add fixture_status.json
git add fixture_user_privilege.json
git add fixture_information_type.json
git add fixture_user_function.json
git add fixture_user_role.json

git commit -m "New data dump"
git push
