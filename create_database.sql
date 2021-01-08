CREATE DATABASE quest;
-- Make sure you've added pg_stat_statements to the
-- shared_preload_libraries setting in postgresql.conf.
CREATE EXTENSION pg_stat_statements
CREATE USER quest with password 'test';
ALTER USER quest CREATEDB;
GRANT ALL PRIVILEGES ON DATABASE quest to quest;
