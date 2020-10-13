# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import logging
from pydantic import ValidationError
from scrapy.exceptions import DropItem
from connectors import db
from .items import Film

# Init logger
logger = logging.getLogger(__name__)


class ValidateDataPipeline:
    def process_item(self, item, spider):
        try:
            film = Film(**item)
            return film
        except ValidationError as e:
            return DropItem


class DbLoadPipeline:
    def process_item(self, item: Film, spider):
        if type(item) == DropItem:
            return item
        try:
            db.insert_film_if_not_exist(db.conn, item)
            return item
        except Exception as e:
            logger.warning(f'Unable to insert element {item}.{e}')
            return e
