CREATE TABLE IF NOT EXISTS (
    id SERIAL PRIMARY KEY,
    store_name TEXT,
    place_id TEXT,
    latitude TEXT,
    longitude TEXT,
    distance_from_origin NUMERIC
);