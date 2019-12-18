#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "root" --dbname "root" <<-EOSQL
    CREATE DATABASE eventio;
    GRANT ALL PRIVILEGES ON DATABASE eventio TO root;
EOSQL