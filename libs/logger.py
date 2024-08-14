import logging
import colorlog
from logging.handlers import RotatingFileHandler
import os, sys


class LoggerFactory(object):
    _LOG = None

    @staticmethod
    def __create_logger(log_folder, log_file, log_level, stdout_flag=False):
        """
        A private method that interacts with the python
        logging module
        """
        full_log_file = os.path.join(log_folder, log_file)
        color_formatter = colorlog.ColoredFormatter(

            "%(cyan)s%(name)s:%(asctime)s%(reset)s | "
            "%(yellow)s%(levelname)s%(reset)s | "
            "%(cyan)s%(filename)s:%(lineno)s%(reset)s | "
            "%(purple)s[%(funcName)s]%(reset)s "
            ">>> %(yellow)s%(message)s%(reset)s"
        )

        file_formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(funcName)s | %(filename)s:%(lineno)s | %(process)d >>> %(message)s"
        )

        file_handler = RotatingFileHandler(full_log_file, backupCount=5, maxBytes=5000000)
        file_handler.setLevel(log_level)
        file_handler.setFormatter(file_formatter)

        # Initialize the class variable with logger object
        log_name = log_file.replace(".log", "")
        LoggerFactory._LOG = logging.getLogger(log_name)
        LoggerFactory._LOG.addHandler(file_handler)
        LoggerFactory._LOG.propagate = False

        if stdout_flag:
            stdout = logging.StreamHandler(stream=sys.stdout)
            stdout.setLevel(log_level)
            stdout.setFormatter(color_formatter)
            LoggerFactory._LOG.addHandler(stdout)

        # set the logging level based on the user selection
        if log_level == "INFO":
            LoggerFactory._LOG.setLevel(logging.INFO)
        elif log_level == "ERROR":
            LoggerFactory._LOG.setLevel(logging.ERROR)
        elif log_level == "DEBUG":
            LoggerFactory._LOG.setLevel(logging.DEBUG)
        return LoggerFactory._LOG

    @staticmethod
    def get_logger(base_path, log_file, log_level, stdout_flag):
        """
        A static method called by other modules to initialize logger in
        their own module
        """
        log_folder = os.path.join(base_path, 'logs')
        os.makedirs(log_folder, exist_ok=True)
        logger = LoggerFactory.__create_logger(log_folder, log_file, log_level, stdout_flag)

        # return the logger object
        return logger
