GRANT ALL PRIVILEGES ON DATABASE postgres TO postgres;

CREATE TABLE IF NOT EXISTS tags(
  name  varchar PRIMARY KEY
);
CREATE TABLE IF NOT EXISTS reviews(
  id      SERIAL PRIMARY KEY,
  tag     varchar REFERENCES tags(name),
  text    varchar
);
