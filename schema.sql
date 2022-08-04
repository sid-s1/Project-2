CREATE TABLE IF NOT EXISTS users (
  id SERIAL PRIMARY KEY,
  first_name TEXT NOT NULL,
  email TEXT NOT NULL,
  password TEXT NOT NULL,
  latitude TEXT NOT NULL,
  longitude TEXT NOT NULL,
  secret TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS stores_1 (
  id SERIAL PRIMARY KEY,
  store_name TEXT NOT NULL,
  place_id TEXT NOT NULL,
  latitude TEXT NOT NULL,
  longitude TEXT NOT NULL,
  distance_from_origin INTEGER NOT NULL,
  user_id INTEGER REFERENCES users(id),
  location TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS items (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    store_id INTEGER REFERENCES stores_1(id),
    item_list TEXT NOT NULL
);