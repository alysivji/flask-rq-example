from flask import jsonify
from flask import blueprints

healthcheck_bp = blueprints.Blueprint('healthcheck', __name__)


@healthcheck_bp.route('/healthcheck', methods=['GET'])
def healthcheck():
    return jsonify({"ping": "pong"})


sandbox_bp = blueprints.Blueprint('sandbox', __name__)


@sandbox_bp.route('/sandbox', methods=['GET'])
def sandbox():
    # TODO Kick off task
    return jsonify({"task": "started"})
