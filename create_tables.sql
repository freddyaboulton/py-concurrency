CREATE TABLE IF NOT EXISTS prices (
    id serial primary key,
    symbol text,
    price float,
    insert_time timestamp
)