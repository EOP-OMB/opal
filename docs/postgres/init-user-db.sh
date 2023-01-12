#!/bin/sh

psql -U postgres <<-EOSQL
    CREATE USER opal;
    CREATE DATABASE opal;
    GRANT ALL PRIVILEGES ON DATABASE opal TO opal;
    GRANT ALL ON SCHEMA public TO opal;
    ALTER ROLE opal WITH PASSWORD '$POSTGRES_OPAL_PASSWORD';
EOSQL