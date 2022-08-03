import logging

logger = logging.getLogger("iTF")


def warning(msg, *args, **kwargs):
    logger.warning(msg, *args, **kwargs)
