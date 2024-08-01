#!/bin/sh

psql -U postgres opal <<-EOSQL
    GRANT ALL PRIVILEGES ON DATABASE opal TO opal;
    GRANT ALL ON SCHEMA public TO opal;
EOSQL