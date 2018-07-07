import sys
import logging


def get_logger(path, level=logging.DEBUG):
    """获取日志"""
    formatter = logging.Formatter('%(asctime)s %(levelname)-8s: %(message)s')
    # console
    console_handler = logging.StreamHandler(sys.stdout)
    # file
    file_handler = logging.FileHandler(path)
    file_handler.setFormatter(formatter)
    logger = logging.getLogger('crawl_gpub')

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    logger.setLevel(level)
    return logger
