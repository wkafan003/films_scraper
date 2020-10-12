from typing import Dict

NAME: str = "films_scraper"

DB_OPTIONS: Dict[str, str] = {
    'dbname': 'postgres',
    'user': 'postgres',
    'host': '127.0.0.1',
    'port': '5432',
    'password': 'PASSWORD',
}
# Configure maximum concurrent requests
CONCURRENT_REQUESTS_PER_DOMAIN = 2
# Start search
START_URLS = [
    'https://www.kinopoisk.ru/popular/films/2018/?page=1&quick_filters=films',
]

# TODO proxy rotator
USE_PROXY = False
PROXIES = {
    'http': 'ip:port',
    'https': 'ip:port',
}
