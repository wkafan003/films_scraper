import logging
import utils.logger as logger
import configurations.settings as settings
from scrapy import cmdline
from connectors.create_db import create_db

# set logger
# comment for use default logger
# logger.init_logger(f'logs/{settings.NAME}.log',logging.WARNING)
create_db('connectors/ddl.sql')
cmdline.execute("scrapy crawl kinopoisk".split())
