# -*- coding: utf-8 -*-
# Author: Riven.FDT
# Description: [utils] Logger module.


import logging.config
import os


class Logger:
    def __init__(self, logger_tag: str) -> None:
        current_abs_dir = os.path.dirname(os.path.realpath(__file__))
        root_abs_dir = os.path.abspath(os.path.join(current_abs_dir, '../../'))

        logger_ini = os.path.join(root_abs_dir, 'conf', 'logger.ini')
        logs_dir = os.path.join(root_abs_dir, 'logs')

        if not os.path.exists(logs_dir):
            os.makedirs(logs_dir)

        logging.config.fileConfig(logger_ini, defaults={'logs_dir': logs_dir})

        self.logger = logging.getLogger(logger_tag)


# Logger for root
root_logger = Logger(logger_tag='root').logger

# Logger for translator
translator_logger = Logger(logger_tag='translator').logger
