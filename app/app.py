import logging
from flask import Flask, request
from rq.handlers import move_to_failed_queue

from .config import DATABASE_URI, REDIS_URI
from .extensions import db, migrate, rq
from .blueprints import healthcheck_bp, sandbox_bp

logger = logging.getLogger(__name__)

rq.exception_handler(move_to_failed_queue)


@rq.exception_handler
def send_alert_to_ops(job, *exc_info):
    print(2)
    logger.error("error occurred")


def create_app(*, testing=False):
    app = Flask(__name__)

    if testing:
        app.config["TESTING"] = True
        database_uri = "sqlite:///:memory:"
    else:
        database_uri = DATABASE_URI

    app.config["SQLALCHEMY_DATABASE_URI"] = database_uri
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    migrate.init_app(app, db)

    app.config['RQ_REDIS_URL'] = REDIS_URI
    app.config['RQ_QUEUES'] = ['default', 'failed']
    app.config['RQ_ASYNC'] = True
    rq.init_app(app)

    app.register_blueprint(healthcheck_bp)
    app.register_blueprint(sandbox_bp)

    @app.before_request
    def add_internal_dictionary():
        """Keep request specific data in `_internal` dictionary"""
        if not getattr(request, "_internal", None):
            request._internal = {}

    return app
