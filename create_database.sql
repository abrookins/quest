CREATE DATABASE quest;
CREATE USER quest with password 'test';
ALTER USER quest CREATEDB;
GRANT ALL PRIVILEGES ON DATABASE quest to quest;
