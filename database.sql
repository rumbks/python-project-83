DROP TABLE IF EXISTS urls;
DROP TABLE IF EXISTS url_checks;

CREATE TABLE urls (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) UNIQUE NOT NULL,
  created_at TIMESTAMP DEFAULT current_timestamp
);

CREATE TABLE url_checks (
  id SERIAL PRIMARY KEY,
  url_id INT NOT NULL,
  status_code INT NOT NULL,
  h1 VARCHAR(255),
  title VARCHAR(512),
  description VARCHAR(1024),
  created_at TIMESTAMP DEFAULT current_timestamp,
  CONSTRAINT fk_url
      FOREIGN KEY(url_id)
	  REFERENCES urls(id)
);
