#!/bin/bash

sudo -u postgres psql <<-EOSQL
    CREATE USER opal;
    CREATE DATABASE opal;
    GRANT ALL PRIVILEGES ON DATABASE opal TO opal;
EOSQL