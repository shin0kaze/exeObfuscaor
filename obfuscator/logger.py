import logging
from logging import debug, info, warning, error, critical

level = logging.INFO

def init(is_debug = False):
    level = logging.DEBUG if is_debug else logging.INFO
    logging.basicConfig(level=level, filename="py_log.log",filemode="a",
                    format="%(asctime)s %(levelname)s %(filename)s:%(funcName)s %(message)s")
    logging.getLogger().addHandler(logging.StreamHandler())

def is_debug():
    return level == logging.DEBUG