from functools import wraps
import psycopg2
import psycopg2.extensions
import connectors
from films_scraper.items import Film
from expiringdict import ExpiringDict

# mem cache dict
cache = ExpiringDict(max_len=10000, max_age_seconds=60*5)

conn: psycopg2.extensions.connection = connectors.conn


def insert_film_if_not_exist(conn: psycopg2.extensions.connection, data: Film) -> None:
    cur: psycopg2.extensions.cursor = conn.cursor()
    film_id: int
    country_id: int

    country_id = iine_country(cur, data.country)

    cur.execute("select id from films where title=%s and country=%s and release_date=%s",
                (data.title, country_id, data.release_date))
    film_id = cur.fetchone()
    if film_id is None:
        cur.execute("insert into films (title, country, box_office, release_date) values (%s,%s,%s,%s) returning id",
                    (data.title, country_id, data.box_office, data.release_date))
        film_id = cur.fetchone()

    type_id: int
    person_id: int
    person2content_exist: bool

    for actor in data.actors:
        type_id = iine_person_type(cur, actor.type)

        cur.execute("select id from persons where fio=%s", (actor.fio,))
        person_id = cur.fetchone()
        if person_id is None:
            cur.execute("insert into persons (fio) values (%s) returning id", (actor.fio,))
            person_id = cur.fetchone()
        cur.connection.commit()

        cur.execute("select count(*) from persons2content where person_id=%s and film_id=%s and person_type=%s",
                    (person_id, film_id, type_id))
        person2content_exist = cur.fetchone()[0] > 0
        if not person2content_exist:
            cur.execute("insert into persons2content (person_id, film_id, person_type)  values (%s,%s,%s)",
                        (person_id, film_id, type_id))
        cur.connection.commit()

    cur.connection.commit()
    cur.close()


def cache_id(func):
    @wraps(func)
    def command_func(cur, obj, *args, **kwargs):
        obj_id = cache.get(obj, None)
        if obj_id is None:
            buf = func(cur, obj)
            cache[obj] = buf
            return buf
        return obj_id

    return command_func


@cache_id
def iine_person_type(cur: psycopg2.extensions.cursor, actor_type: str) -> int:
    cur.execute("select id from person_types where type=%s", (actor_type,))
    type_id = cur.fetchone()
    if type_id is None:
        cur.execute("insert into person_types (type) values (%s) returning id", (actor_type,))
        type_id = cur.fetchone()
    cur.connection.commit()
    return type_id


@cache_id
def iine_country(cur: psycopg2.extensions.cursor, country: str) -> int:
    cur.execute("select id from countries where name=%s", (country,))
    country_id = cur.fetchone()
    if country_id is None:
        cur.execute("insert into countries (name) values (%s) returning id", (country,))
        country_id = cur.fetchone()
    cur.connection.commit()
    return country_id
