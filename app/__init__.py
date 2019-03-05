import logging

logger = logging.getLogger(__name__)

logger.info("Starting Server")
from .app import create_app  # noqa
app = create_app()
from .models import *  # noqa
