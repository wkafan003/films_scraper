==========
film_scraper
==========

.. image:: https://github.com/wkafan003/films_scraper/blob/master/assets/logo.png?raw=true
   :align: center
==========
Установка
==========

Установка зависимостей через pip

.. code:: shell

    $ pip install -r requirements.txt 

==========
Настройка
==========
В файле настроек ``/configurations/settings.py`` задаются настройки подключение к базе данных, настройки прокси, начальная страница для загрузки фильмов (по умолчанию бот сканирует лучшие фильмы 2018 года)


.. code:: python

  from typing import Dict

  NAME: str = "films_scraper"

  DB_OPTIONS: Dict[str, str] = {
      'dbname': 'postgres',
      'user': 'postgres',
      'host': '127.0.0.1',
      'port': '5432',
      'password': '123',
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
