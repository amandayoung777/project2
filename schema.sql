DROP TABLE IF EXISTS food;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT NOT NULL,
    firstname TEXT NOT NULL,
    lastname TEXT NOT NULL,
    email TEXT,
    password TEXT,
    admin TEXT    
);

CREATE TABLE food (
    id serial PRIMARY KEY,
    name varchar(50) NOT NULL,
    mood text
);

