import sys

from loguru import logger

import config


def setup():
    log_path = config.app_dir / 'log'
    log_path.mkdir(parents=True, exist_ok=True)
    logger.add(
            sink=log_path / config.PRINT_LOG,
            format='{time} - {name} - {level} - {message}',
            level="DEBUG")
    logger.info("Program started")
    if config.CAPTURE_STD_ERR:
        sys.stderr = open(log_path / config.ERR_LOG, 'a')
