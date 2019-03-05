import logging
import time
from .extensions import rq

logger = logging.getLogger(__name__)


@rq.job
def add(x, y):
    result = x + y
    time.sleep(5)
    logger.info(result)
    raise ValueError
    return result
