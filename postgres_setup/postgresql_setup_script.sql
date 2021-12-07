CREATE DATABASE opal;
CREATE USER opal_user WITH PASSWORD 'use_a_strong_password';
ALTER ROLE opal_user SET client_encoding TO 'utf8';
ALTER ROLE opal_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE opal_user SET timezone TO 'EST';
GRANT ALL PRIVILEGES ON DATABASE opal TO opal_user;
