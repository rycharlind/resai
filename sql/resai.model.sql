drop table if exists resai_users cascade;

create table resai_users (
  id serial primary key,
  username varchar(50) not null unique,
  password_hash char(60) not null,
  email varchar(255) not null unique,
  created_at timestamp default now()
);

insert into resai_users (username, password_hash, email) values ('admin', 'admin', 'admin@email.com');

drop table if exists resai_documents cascade;

create table resai_documents (
  id serial primary key,
  user_id integer not null,
  file_key varchar(255) not null,
  file_name varchar(255) not null,
  file_size integer not null,
  content_type varchar(255) not null,
  created_at timestamp default now(),
  foreign key (user_id) references resai_users(id) on delete cascade
);

drop table if exists resai_collections cascade;

create table resai_collections (
  id serial primary key,
  name varchar(50) not null unique,
  description text,
  created_at timestamp default now()
);

drop table if exists resai_users_collections cascade;

create table resai_users_collections (
  user_id integer not null,
  collection_id integer not null,
  foreign key (user_id) references resai_users(id) on delete cascade,
  foreign key (collection_id) references resai_collections(id) on delete cascade,
  primary key (user_id, collection_id)
);

-- create a collections to 