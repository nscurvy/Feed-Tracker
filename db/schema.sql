-- @formatter:off
CREATE TABLE if NOT EXISTS animal_type (
    animal_type_id INTEGER PRIMARY KEY,
    animal_name TEXT NOT NULL
);

CREATE TABLE if NOT EXISTS animal_population (
    animal_type_id INTEGER PRIMARY KEY,
    quantity INTEGER NOT NULL,
    date_updated DATE NOT NULL,
    FOREIGN KEY(animal_type_id) REFERENCES animal_type(animal_type_id)
);

CREATE TABLE if NOT EXISTS animal_population_update (
    id INTEGER PRIMARY KEY,
    animal_type_id INTEGER NOT NULL,
    delta INTEGER NOT NULL,
    update_date DATE NOT NULL,
    reason TEXT,
    FOREIGN KEY(animal_type_id) REFERENCES animal_type(animal_type_id)
);

CREATE TABLE IF NOT EXISTS feed (
    feed_id INTEGER PRIMARY KEY,
    animal_type_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    FOREIGN KEY(animal_type_id) REFERENCES animal_type(animal_type_id)
);

CREATE TABLE IF NOT EXISTS source (
    source_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS unit (
    unit_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    conversion_factor REAL NOT NULL
);
