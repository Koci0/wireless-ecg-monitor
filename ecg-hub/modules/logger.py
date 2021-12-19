
from modules.const import LOG_TO_FILE

import logging

from datetime import datetime


class Logger:

    def __init__(self, filename=f"log_{datetime.now()}"):
        if LOG_TO_FILE:
            logging.basicConfig(filename=filename, level=logging.INFO)
        else:
            logging.basicConfig(level=logging.INFO)

        self.logger = logging.getLogger(__name__)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)
