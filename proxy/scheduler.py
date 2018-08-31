#!/usr/bin/env python
# coding=utf-8

import time
import sys
import schedule
#sys.path.append("..")
from proxy.config import CRAWLER_RUN_CYCLE, VALIDATOR_RUN_CYCLE

from proxy.crawler import crawler
from proxy.validator import validator
from proxy.logger import logger


def run_schedule():
    """
    启动客户端
    """
    # 启动收集器
    schedule.every(CRAWLER_RUN_CYCLE).minutes.do(crawler.run).run()
    # 启动验证器
    schedule.every(VALIDATOR_RUN_CYCLE).minutes.do(validator.run).run()

    while True:
        try:
            schedule.run_pending()
            time.sleep(1)
        except KeyboardInterrupt:
            logger.info("You have canceled all jobs")
            return
