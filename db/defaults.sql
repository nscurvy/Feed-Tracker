INSERT INTO unit (name, type, conversion_factor) VALUES
    ('lb', 'mass', 1.0),
    ('quart', 'volume', 0.25),
    ('gallon', 'volume', 1.0)
ON CONFLICT DO NOTHING;

INSERT INTO source (name) VALUES
    ('tsc'),
    ('amazon'),
    ('elma f&f')
ON CONFLICT DO NOTHING;

INSERT INTO animal_type (name) VALUES ('duck') ON CONFLICT DO NOTHING;

INSERT INTO feed (name, animal_type_id)
SELECT v.column1, at.animal_type_id
FROM animal_type AS at
         JOIN (
    VALUES
        ('pellets'),
        ('mealworms'),
        ('bsf'),
        ('scratch')
) v
WHERE at.name = 'duck'
ON CONFLICT DO NOTHING;

