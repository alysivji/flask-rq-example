import logging
from .extensions import rq

logger = logging.getLogger(__name__)


@rq.job
def add(x, y):
    result = x + y
    logger.info(result)
    raise ValueError
    return result
