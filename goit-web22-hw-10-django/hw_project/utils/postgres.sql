CREATE TABLE authors (
    id SERIAL PRIMARY KEY,
    fullname VARCHAR(255) NOT NULL,
    born_date DATE,
    born_location VARCHAR(255),
    description TEXT
);

CREATE TABLE quotes (
    id SERIAL PRIMARY KEY,
    quote TEXT NOT NULL,
    author_id INTEGER REFERENCES authors(id),
    tags VARCHAR(255)[]
);
