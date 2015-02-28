-- name: create_person_table
CREATE TABLE person (
	person_id INTEGER NOT NULL GENERATED ALWAYS AS IDENTITY,
	name VARCHAR(20) UNIQUE NOT NULL,
	age INTEGER NOT NULL
)

-- name: insert_person
INSERT INTO person (
	name,
	age
) VALUES (
	%(name)s,
	%(age)s
)

-- name: find_older_than
SELECT *
FROM person
WHERE age > %s

-- name: find_by_age
SELECT *
FROM person
WHERE age IN (%s)

-- name: update_age
UPDATE person
SET age = %(age)s
WHERE name = %(name)s

-- name: delete_person
DELETE FROM person
WHERE name = %s

-- name: drop_person_table
-- completely destroys the person table!
DROP TABLE person
