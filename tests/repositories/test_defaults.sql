-- PRAGMA foreign_keys = ON;

BEGIN TRANSACTION;

-- --------------------
-- Animal types
-- --------------------
INSERT INTO animal_type (name) VALUES
                                   ('duck'),
                                   ('cat');

-- --------------------
-- Units
-- --------------------
INSERT INTO unit (name, type, conversion_factor) VALUES
                                                     ('lb', 'mass', 1.0),
                                                     ('kg', 'mass', 2.20462),
                                                     ('g', 'mass', 0.00220462),
                                                     ('oz', 'mass', 0.0625),
                                                     ('cup', 'volume', 1.0);

-- --------------------
-- Sources
-- --------------------
INSERT INTO source (name) VALUES
                              ('Tractor Supply Co'),
                              ('Local Feed Store'),
                              ('Online Retailer');

-- --------------------
-- Feeds
-- --------------------
INSERT INTO feed (animal_type_id, name)
SELECT animal_type_id, 'pellets'
FROM animal_type WHERE name = 'duck';

INSERT INTO feed (animal_type_id, name)
SELECT animal_type_id, 'mealworms'
FROM animal_type WHERE name = 'duck';

INSERT INTO feed (animal_type_id, name)
SELECT animal_type_id, 'dry kibble'
FROM animal_type WHERE name = 'cat';

-- --------------------
-- Feed products
-- --------------------
-- Duck pellets: two brands, same source, same unit/quantity
INSERT INTO feed_product (
    feed_id, quantity, unit_id, source_id, brand_name, cost_cents, date_updated
)
SELECT
    f.feed_id,
    50,
    u.unit_id,
    s.source_id,
    'Purina',
    2499,
    '2025-01-05'
FROM feed f
         JOIN unit u ON u.name = 'lb' AND u.type = 'mass'
         JOIN source s ON s.name = 'Tractor Supply Co'
WHERE f.name = 'pellets';

INSERT INTO feed_product (
    feed_id, quantity, unit_id, source_id, brand_name, cost_cents, date_updated
)
SELECT
    f.feed_id,
    50,
    u.unit_id,
    s.source_id,
    'Nutrena',
    2699,
    '2025-01-05'
FROM feed f
         JOIN unit u ON u.name = 'lb' AND u.type = 'mass'
         JOIN source s ON s.name = 'Tractor Supply Co'
WHERE f.name = 'pellets';

-- Mealworms
INSERT INTO feed_product (
    feed_id, quantity, unit_id, source_id, brand_name, cost_cents, date_updated
)
SELECT
    f.feed_id,
    5,
    u.unit_id,
    s.source_id,
    'HappyHen',
    1899,
    '2025-01-10'
FROM feed f
         JOIN unit u ON u.name = 'lb' AND u.type = 'mass'
         JOIN source s ON s.name = 'Online Retailer'
WHERE f.name = 'mealworms';

-- Cat food
INSERT INTO feed_product (
    feed_id, quantity, unit_id, source_id, brand_name, cost_cents, date_updated
)
SELECT
    f.feed_id,
    20,
    u.unit_id,
    s.source_id,
    'Blue Buffalo',
    3299,
    '2025-01-03'
FROM feed f
         JOIN unit u ON u.name = 'lb' AND u.type = 'mass'
         JOIN source s ON s.name = 'Local Feed Store'
WHERE f.name = 'dry kibble';

-- --------------------
-- Feed product updates (tests trigger)
-- --------------------
INSERT INTO feed_product_update (
    feed_product_id, new_cost_cents, date_updated
)
SELECT
    feed_product_id,
    cost_cents + 200,
    '2025-02-01'
FROM feed_product
WHERE brand_name = 'Purina';

-- --------------------
-- Purchases
-- --------------------
INSERT INTO purchase (feed_product_id, quantity, purchase_date)
SELECT
    feed_product_id,
    2,
    '2025-02-02'
FROM feed_product
WHERE brand_name = 'Purina';

INSERT INTO purchase (feed_product_id, quantity, purchase_date)
SELECT
    feed_product_id,
    1,
    '2025-02-05'
FROM feed_product
WHERE brand_name = 'HappyHen';

-- --------------------
-- Animal population updates (tests trigger)
-- --------------------
INSERT INTO animal_population_update (
    animal_type_id, delta, date_updated, reason
)
SELECT
    animal_type_id,
    6,
    '2025-01-01',
    'Initial flock'
FROM animal_type WHERE name = 'duck';

INSERT INTO animal_population_update (
    animal_type_id, delta, date_updated, reason
)
SELECT
    animal_type_id,
    -1,
    '2025-02-15',
    'Predation'
FROM animal_type WHERE name = 'duck';

INSERT INTO animal_population_update (
    animal_type_id, delta, date_updated, reason
)
SELECT
    animal_type_id,
    2,
    '2025-01-01',
    'Adopted cats'
FROM animal_type WHERE name = 'cat';

-- --------------------
-- Consumption
-- --------------------
INSERT INTO consumption (
    feed_id, quantity, unit_id, animal_type_id, consumption_date, note
)
SELECT
    f.feed_id,
    1.5,
    u.unit_id,
    a.animal_type_id,
    '2025-02-03',
    'Morning feeding'
FROM feed f
         JOIN unit u ON u.name = 'lb' AND u.type = 'mass'
         JOIN animal_type a ON a.name = 'duck'
WHERE f.name = 'pellets';

INSERT INTO consumption (
    feed_id, quantity, unit_id, animal_type_id, consumption_date, note
)
SELECT
    f.feed_id,
    0.25,
    u.unit_id,
    a.animal_type_id,
    '2025-02-03',
    'Treats'
FROM feed f
         JOIN unit u ON u.name = 'lb' AND u.type = 'mass'
         JOIN animal_type a ON a.name = 'duck'
WHERE f.name = 'mealworms';

COMMIT;
