# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from typing import List
from pydantic import BaseModel, constr, conint


class Actor(BaseModel):
    type: constr(max_length=50) = 'Не указано'
    fio: constr(max_length=100) = 'Не указано'


class Film(BaseModel):
    title: constr(max_length=50) = 'Не указано'
    country: constr(max_length=64) = 'Не указано'
    release_date: conint(ge=0) = 0
    box_office: conint(ge=0) = 0
    actors: List[Actor]
