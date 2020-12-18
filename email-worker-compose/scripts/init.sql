DROP DATABASE IF EXISTS email_sender;
CREATE DATABASE email_sender;

\c email_sender

create table if not exists emails (
    id serial not null,
    data timestamp not null default current_timestamp,
    subject varchar(100) not null,
    message varchar(259) not null
);