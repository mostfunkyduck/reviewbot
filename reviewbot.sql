GRANT ALL PRIVILEGES ON DATABASE postgres TO postgres;
CREATE TABLE IF NOT EXISTS reviews(
  id      SERIAL PRIMARY KEY,
  tag     varchar,
  text    varchar
)
