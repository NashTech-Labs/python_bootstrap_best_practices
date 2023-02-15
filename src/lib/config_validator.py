"""Module to validate the config file"""
import logging
import os
import re
import sys
import traceback
from configparser import ConfigParser


class ConfigValidator:
    """Class to validate config"""

    def __init__(self):
        self.__filename = "config.ini"
        self.__config_directory = "config/"
        self.__config_directory_path = os.path.dirname(os.path.dirname(__file__))

        self.__config_keys = [
            "max_content_length_mib",
            "upload_folder",
            "extract_folder",
            "model_path",
            "host",
            "port",
            "extensions",
            "log_level",
        ]

        self.__error_message = "Config Validation Failed"
        self.__log_levels = [
            "CRITICAL",
            "FATAL",
            "ERROR",
            "WARN",
            "WARNING",
            "INFO",
            "DEBUG",
            "NOTSET",
        ]

    def __validate(self):
        file = os.path.join(self.__config_directory_path, self.__config_directory, self.__filename)

        # validating file
        assert os.path.exists(file), self.__error_message

        cnf_parser = ConfigParser()
        cnf_parser.read(file)
        config = cnf_parser.defaults()  # type: dict

        # validating default section
        assert config != {}, self.__error_message

        # validating keys
        for key in config.keys():
            assert key in self.__config_keys, self.__error_message

        # validating values
        assert config["log_level"] in self.__log_levels
        assert config["max_content_length_mib"] <= "50", self.__error_message
        # print(os.path.join(self.__config_directory_path, config["upload_folder"]))
        assert os.path.exists(
            os.path.join(self.__config_directory_path, config["upload_folder"])
        ), self.__error_message
        assert os.path.exists(
            os.path.join(self.__config_directory_path, config["extract_folder"])
        ), self.__error_message
        assert os.path.exists(
            os.path.join(self.__config_directory_path, config["model_path"])
        ), self.__error_message

        if "host" not in config.keys():
            config["host"] = "localhost"

        if "port" not in config.keys():
            config["port"] = "4000"

        extensions = config["extensions"].split(",")
        regex = re.compile("[^A-Za-z0-9]")
        for extension in extensions:
            assert not regex.search(extension.strip()), self.__error_message

        return config

    def validate_and_getconfig(self):
        """validate and get the config file"""
        try:
            conf = self.__validate()
            conf["upload_folder"] = os.path.join(
                self.__config_directory_path, conf["upload_folder"]
            )
            conf["extract_folder"] = os.path.join(
                self.__config_directory_path, conf["extract_folder"]
            )
            conf["model_path"] = os.path.join(self.__config_directory_path, conf["model_path"])
            conf["max_content_length_mib"] = int(conf["max_content_length_mib"]) * 1024 * 1024
            conf["extensions"] = [extension.strip() for extension in conf["extensions"].split(",")]
            return conf
        except AssertionError:
            logging.error(traceback.format_exc())
            logging.fatal("Aborting...")
            sys.exit("Aborting...")
        except Exception as error:
            logging.error(error)
            logging.error(traceback.format_exc())
            logging.fatal("Aborting...")
            sys.exit("Aborting...")
