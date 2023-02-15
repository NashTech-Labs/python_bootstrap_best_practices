""" Module providing logging capabilities"""
import logging
import os
import time


class Logger:
    """class:logger"""

    def __init__(self):
        """creates a logfile default dir and defines log levels"""
        self.__log_file_directory = "logs/"
        self.__log_file_name = time.strftime("%Y_%m_%d") + ".log"
        self.__log_file_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))),
            self.__log_file_directory,
            self.__log_file_name,
        )
        self.__log_levels = {
            "CRITICAL": 50,
            "FATAL": 50,
            "ERROR": 40,
            "WARN": 30,
            "WARNING": 30,
            "INFO": 20,
            "DEBUG": 10,
            "NOTSET": 0,
        }

    def initialize(self):
        """
        creates a logfile
        :return:
        """
        logging.basicConfig(
            filename=self.__log_file_path,
            filemode="a",
            level=logging.DEBUG,
            format="%(asctime)s %(levelname)-8s %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        logging.info("Initializing ...")
        logging.info(f"Logging to {self.__log_file_path}")

    def set_log_level(self, level: str):
        """
        :param level: log level
        :return:
        """
        logger = logging.getLogger()
        logger.setLevel(self.__log_levels[level])
        logging.info(f"Log level is set to {level}:{self.__log_levels[level]}")
