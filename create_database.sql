CREATE DATABASE studyup;
CREATE USER studyup with password 'test';
ALTER USER studyup CREATEDB;
GRANT ALL PRIVILEGES ON DATABASE studyup to studyup;
