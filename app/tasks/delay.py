import logging
import sys
import time

from flask import current_app as app  # noqa

from .utilities import _set_task_progress
from app.extensions import rq

logger = logging.getLogger(__name__)


@rq.job
def delay(seconds):
    try:
        for elapsed_time in range(seconds):
            time.sleep(1)
            logger.info(f"Time elapsed:{elapsed_time} seconds")
            _set_task_progress((elapsed_time + 1) / seconds * 100)
    except:  # noqa
        _set_task_progress(100)
        logging.error('Unhandled exception', exc_info=sys.exc_info())

    return seconds


@rq.job
def delay_error(seconds):
    raise ValueError
