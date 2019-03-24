import logging
from logging.config import dictConfig as load_dict_config
from flask import Flask, request

from .config import DATABASE_URI, REDIS_URI, LOGGING_CONFIG
from .extensions import db, migrate, rq
from .blueprints import healthcheck_bp, sandbox_bp

load_dict_config(LOGGING_CONFIG)
logger = logging.getLogger(__name__)


def create_app(*, testing=False):
    app = Flask(__name__)

    if testing:
        app.config["TESTING"] = True
        database_uri = "sqlite:///:memory:"

        app.config['RQ_CONNECTION_CLASS'] = 'fakeredis.FakeStrictRedis'
        app.config['RQ_ASYNC'] = True
        redis_uri = "redis"
    else:
        database_uri = DATABASE_URI
        redis_uri = REDIS_URI

    app.config["SQLALCHEMY_DATABASE_URI"] = database_uri
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    migrate.init_app(app, db)

    app.config['RQ_REDIS_URL'] = redis_uri
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
