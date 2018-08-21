#!/usr/bin/env python3
# coding = utf-8

import logging
import time
import os


def get_logger():
    """
    创建日志
    """
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    rq = time.strftime('%Y%m%d%H', time.localtime(time.time()))
    log_path = os.path.dirname(os.getcwd()) + '/Logs/'
    log_name = log_path + rq + '.log'
    fh = logging.FileHandler(log_name)
    fh.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s'\
        '- %(filename)s:[line:%(lineno)s]'\
        '- %(levelname)s - %(message)s')
    fh.setFormatter(formatter)

    logger.addHandler(fh)
    return logger

logger=get_logger()