CREATE SCHEMA shop;

DROP TABLE IF EXISTS shop.cities CASCADE;
CREATE TABLE shop.cities (
	id serial8 NOT NULL,
	country varchar(255) NOT NULL,
	state varchar(255) NOT NULL,
	city varchar(255) NOT NULL,
	created_at timestamp default current_timestamp,
	primary key (id)
);


CREATE TYPE GENDER AS ENUM ('male', 'female');
-- DROP TABLE shop.users CASCADE;
CREATE TABLE IF NOT EXISTS shop.users (
    "id" serial8 NOT NULL,
    "email" varchar(255) NOT NULL,
    "name" varchar(255) NULL,
    "last_name" varchar(255) NULL,
    "phone_number" varchar(255) NOT NULL,
    "gender" gender NULL,
    "hashed_password" varchar(255) NULL,
    "created_at" timestamp(6) NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" timestamp(6) NULL,
    "deleted_at" timestamp(6) NULL,
    CONSTRAINT users_email_key UNIQUE (email),
    CONSTRAINT users_pkey PRIMARY KEY (id)
);

--DROP TABLE IF EXISTS shop.categories CASCADE;
CREATE TABLE shop.categories (
	id serial8 NOT NULL,
	title varchar(255) NOT NULL,
	description text,
	created_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY(id)
);

--DROP TABLE shop.products CASCADE;
CREATE TABLE shop.products (
	id serial8 NOT NULL,
	is_active bool NOT NULL DEFAULT false,
	title varchar(255) NOT NULL,
	price int8 NOT NULL,
	description text NULL,
	city int4 NULL,
	category int4 NOT NULL,
	image varchar(255) NULL,
	created_at timestamp NULL DEFAULT CURRENT_TIMESTAMP,
	"owner" int8 NOT NULL,
	CONSTRAINT products_pk PRIMARY KEY (id),
	CONSTRAINT fk_owner FOREIGN KEY ("owner") REFERENCES shop.users(id) ON DELETE CASCADE ON UPDATE cascade,
	CONSTRAINT fk_city FOREIGN KEY ("city") REFERENCES shop.cities(id) ON DELETE CASCADE ON UPDATE cascade,
	constraint fk_category FOREIGN KEY ("category") REFERENCES shop.categories(id) ON DELETE CASCADE ON UPDATE cascade
);
