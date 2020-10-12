from scrapy import cmdline
import utils.logger as logger
import configurations.settings as settings
import logging

# set logger
# comment for use default logger
# logger.init_logger(f'logs/{settings.NAME}.log',logging.WARNING)
cmdline.execute("scrapy crawl kinopoisk".split())
