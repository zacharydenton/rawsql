-- name: fetch_by_id
-- retrieves a single record by id.
select id, uuid from items where id = ?;
