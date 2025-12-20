-- @formatter:off
CREATE TABLE IF NOT EXISTS animal_type (
    animal_type_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE if NOT EXISTS animal_population (
    animal_type_id INTEGER PRIMARY KEY,
    quantity INTEGER NOT NULL,
    date_updated TEXT NOT NULL,
    FOREIGN KEY(animal_type_id) REFERENCES animal_type(animal_type_id)
);

CREATE TABLE if NOT EXISTS animal_population_update (
    id INTEGER PRIMARY KEY,
    animal_type_id INTEGER NOT NULL,
    delta INTEGER NOT NULL,
    update_date TEXT NOT NULL,
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

CREATE TABLE IF NOT EXISTS purchase (
    purchase_id INTEGER PRIMARY KEY,
    feed_id INTEGER NOT NULL,
    source_id INTEGER NOT NULL,
    quantity REAL NOT NULL,
    unit_id INTEGER NOT NULL,
    cost REAL NOT NULL,
    purchase_date TEXT NOT NULL,
    FOREIGN KEY(feed_id) REFERENCES feed(feed_id),
    FOREIGN KEY(source_id) REFERENCES source(source_id),
    FOREIGN KEY(unit_id) REFERENCES unit(unit_id)
    );

CREATE TABLE IF NOT EXISTS consumption (
    consumption_id INTEGER PRIMARY KEY,
    feed_id INTEGER NOT NULL,
    quantity REAL NOT NULL,
    unit_id INTEGER NOT NULL,
    animal_type_id INTEGER NOT NULL,
    consumption_date TEXT NOT NULL,
    note TEXT,
    FOREIGN KEY(feed_id) REFERENCES feed(feed_id),
    FOREIGN KEY(animal_type_id) REFERENCES animal_type(animal_type_id),
    FOREIGN KEY(unit_id) REFERENCES unit(unit_id)
);
