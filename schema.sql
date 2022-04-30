DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS food;

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT,
    password TEXT,
    admin TEXT    
);

CREATE TABLE food (
    id serial PRIMARY KEY,
    name varchar(50) NOT NULL,
    mood text
);

