CREATE USER reviewbot WITH PASSWORD 'yaakov';
CREATE DATABASE reviewbot;
GRANT ALL PRIVILEGES ON DATABASE reviewbot TO reviewbot;

CREATE TABLE reviews(
  reviewtext  varchar
)
