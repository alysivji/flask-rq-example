from flask import jsonify
from flask import blueprints

from .tasks import add

healthcheck_bp = blueprints.Blueprint('healthcheck', __name__)


@healthcheck_bp.route('/healthcheck', methods=['GET'])
def healthcheck():
    return jsonify({"ping": "pong"})


sandbox_bp = blueprints.Blueprint('sandbox', __name__)


@sandbox_bp.route('/sandbox', methods=['GET'])
def sandbox():
    # TODO Kick off task
    job = add.queue(1, 2)
    return jsonify({"task": "started"})
