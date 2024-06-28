import logging


def get_logger(name):
    logger = logging.Logger(name)
    formatter = logging.Formatter(
        'time=%(asctime)s '
        'level=%(levelname)s '
        'module=%(module)s:%(funcName)s '
        'msg="%(message)s" '
    )
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    logger = logging.LoggerAdapter(logger=logger, extra={})
    return logger
