create table if not exists countries
(
	id serial not null
		constraint countries_pk
			primary key,
	name varchar(64)
);

alter table countries owner to postgres;

create unique index if not exists countries_name_uindex
	on countries (name);

create table if not exists persons
(
	id serial not null
		constraint persons_pk
			primary key,
	fio varchar(100)
);

alter table persons owner to postgres;

create table if not exists films
(
	id serial not null
		constraint films_pk
			primary key,
	title varchar(50) default 'Не указано'::character varying not null,
	country integer not null
		constraint films_countries_id_fk
			references countries
				on update cascade on delete restrict,
	box_office integer default 0,
	release_date integer
);

alter table films owner to postgres;

create table if not exists person_types
(
	id serial not null
		constraint person_types_pk
			primary key,
	type varchar(50) not null
);

alter table person_types owner to postgres;

create unique index if not exists person_types_type_uindex
	on person_types (type);

create table if not exists  persons2content
(
	person_id integer not null
		constraint persons2content_persons_id_fk
			references persons,
	film_id integer not null
		constraint persons2content_films_id_fk
			references films,
	person_type integer
		constraint persons2content_person_types_id_fk
			references person_types,
	constraint persons2content_pk
		unique (person_id, film_id, person_type)
);

alter table persons2content owner to postgres;
