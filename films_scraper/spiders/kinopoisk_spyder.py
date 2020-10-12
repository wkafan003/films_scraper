from typing import Dict
import re
import scrapy
import logging
import configurations.settings as settings

# Init logger
logger = logging.getLogger(__name__)


class KinipoiskSpider(scrapy.Spider):
    name = "kinopoisk"
    # start_urls = [
    #     'https://www.kinopoisk.ru/index.php?level=7&from=forma&result=adv&m_act%5Bfrom%5D=forma&m_act%5Bwhat%5D=content&m_act%5Bfind%5D=%F8%F0%E5%EA',
    # 'https://www.kinopoisk.ru/popular/films/2016/?page=1&quick_filters=films',
    # ]
    start_urls = settings.START_URLS
    re_film = re.compile('^.*/film/\d+.?$')

    def parse(self, response: scrapy.http.TextResponse, **kwargs):
        all_a = response.xpath('//a')
        # if a href contain *film/int_id/ then it is film link
        films = [a.attrib['href'] for a in all_a if self.re_film.match(a.attrib.get('href', '')) is not None]
        for film in films:
            f = response.urljoin(film)
            yield scrapy.Request(f, callback=self.parse_film)
        next_page = response.xpath("//a[contains(text(),'Вперёд')]/@href").get()
        if next_page:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_film(self, response: scrapy.http.TextResponse, **kwargs):
        title = None
        try:
            title = response.xpath("//span[@class='styles_title__2l0HH']/text()").get()
            release_date = response.xpath('//div[text()="Год производства"]/../div[2]/a/text()').get()
            country = response.xpath('//div[text()="Страна"]/../div[2]/a/text()').get()
            box_office = response.xpath('//div[text()="Сборы в мире"]/../div[2]/a/text()').get()

            if title is None:
                raise Exception('Ну удалось получить название')
            if country is None:
                country = 'Не указано'
                self.logger.warning('Не удалось получить страну')
            if release_date is None:
                release_date = '0000'
                self.logger.warning('Не удалось получить год производства')
            if box_office is None:
                box_office = '0'
                self.logger.warning('Не удалось получить сборы в мире')
            else:
                buf = box_office.rfind('$')
                box_office = ''.join(box_office[buf + 1:].split())
            film_data = {'title': title, 'release_date': release_date,
                         'country': country, 'box_office': box_office}
            yield scrapy.Request(response.url + 'cast/', callback=self.parse_actors, cb_kwargs={'film_data': film_data})

        except Exception as e:
            self.logger.warning(f'Cannot parse film_data {title if title else "Название не определно "}')
            self.logger.warning(str(e))

    def parse_actors(self, response: scrapy.http.TextResponse, film_data: Dict, **kwargs):
        film_data['actors'] = []
        actors_block = response.xpath('//div[@class="block_left"]/*')
        actor_type = 'Не указано'
        buf_type: str
        actor_fio: str
        for i in actors_block:
            if i.root.tag == 'a':
                buf_type = i.xpath('@name').get()
                if buf_type is None:
                    self.logger.warning(f'Ошибка добавления должности актера {str(i)}')
                else:
                    actor_type = buf_type
            if len(i.css('div.dub')) == 1:
                actor_fio = i.css('div.name a::text').get()
                if actor_fio is None:
                    self.logger.warning(f'Ошибка добавления актера {str(i)}')
                else:
                    film_data['actors'].append({'type': actor_type, 'fio': actor_fio})
        self.logger.debug(f'Фильм {film_data["title"]} загружен.')
        yield film_data
