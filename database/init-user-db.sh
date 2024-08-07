#!/bin/bash
set -e

# todo(berry): make user and database variables
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
	CREATE USER amt WITH PASSWORD 'changethis' CREATEDB;
	CREATE DATABASE amt OWNER amt;
EOSQL
