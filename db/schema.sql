CREATE TABLE IF NOT EXISTS animal_type (
    animal_type_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS animal_population (
    animal_type_id INTEGER PRIMARY KEY,
    quantity INTEGER NOT NULL,
    date_updated TEXT NOT NULL,
    FOREIGN KEY(animal_type_id) REFERENCES animal_type(animal_type_id)
);

CREATE TABLE IF NOT EXISTS animal_population_update (
    id INTEGER PRIMARY KEY,
    animal_type_id INTEGER NOT NULL,
    delta INTEGER NOT NULL CHECK (delta <> 0),
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

CREATE TABLE feed_product (
    feed_product_id INTEGER PRIMARY KEY,
    feed_id INTEGER NOT NULL,
    quantity REAL NOT NULL CHECK (quantity > 0),
    unit_id INTEGER NOT NULL,
    source_id INTEGER NOT NULL,
    cost_cents INTEGER NOT NULL CHECK (cost_cents > 0),
    date_updated TEXT NOT NULL,
    FOREIGN KEY(feed_id) REFERENCES feed(feed_id),
    FOREIGN KEY(unit_id) REFERENCES unit(unit_id),
    FOREIGN KEY(source_id) REFERENCES source(source_id)
);

CREATE TABLE feed_product_update (
    id INTEGER PRIMARY KEY,
    feed_product_id INTEGER NOT NULL,
    new_cost_cents INTEGER NOT NULL CHECK (new_cost_cents > 0),
    date_updated TEXT NOT NULL,
    FOREIGN KEY(feed_product_id) REFERENCES feed_product(feed_product_id)
);

CREATE TABLE IF NOT EXISTS source (
    source_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS unit (
    unit_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    type TEXT NOT NULL,
    conversion_factor REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS purchase (
    purchase_id INTEGER PRIMARY KEY,
    feed_product_id INTEGER NOT NULL,
    purchase_date TEXT NOT NULL,
    FOREIGN KEY(feed_product_id) REFERENCES feed_product(feed_product_id)
);

CREATE TABLE IF NOT EXISTS consumption (
    consumption_id INTEGER PRIMARY KEY,
    feed_id INTEGER NOT NULL,
    quantity REAL NOT NULL CHECK (quantity > 0),
    unit_id INTEGER NOT NULL,
    animal_type_id INTEGER NOT NULL,
    consumption_date TEXT NOT NULL,
    note TEXT,
    FOREIGN KEY(feed_id) REFERENCES feed(feed_id),
    FOREIGN KEY(animal_type_id) REFERENCES animal_type(animal_type_id),
    FOREIGN KEY(unit_id) REFERENCES unit(unit_id)
);

-- Indexes

CREATE INDEX idx_purchase_date ON purchase(purchase_date);
CREATE INDEX idx_consumption_date ON consumption(consumption_date);
CREATE INDEX idx_purchase_feed ON purchase(feed_id);
CREATE INDEX idx_consumption_feed ON consumption(feed_id);

-- Triggers

CREATE TRIGGER update_population_after_insert
AFTER INSERT ON animal_population_update
BEGIN
    INSERT INTO animal_population (animal_type_id, quantity, date_updated)
    VALUES (NEW.animal_type_id, NEW.delta, NEW.update_date)
    ON CONFLICT(animal_type_id) DO UPDATE SET
        quantity = quantity + NEW.delta,
        date_updated = NEW.update_date;
END;
