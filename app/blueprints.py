import logging
import uuid

from flask import jsonify
from flask import blueprints

from .extensions import db
from .models import Task, User
from .tasks import delay, delay_error

logger = logging.getLogger(__name__)
healthcheck_bp = blueprints.Blueprint('healthcheck', __name__)


@healthcheck_bp.route('/healthcheck', methods=['GET'])
def healthcheck():
    logger.info("[Web] Hit healthcheck endpoint")
    return jsonify({"ping": "pong"})


sandbox_bp = blueprints.Blueprint('sandbox', __name__)


@sandbox_bp.route('/sandbox', methods=['GET'])
def sandbox():
    logger.info("[Web] Hit sandbox endpoint")

    user = User(email=str(uuid.uuid4()))
    db.session.add(user)
    db.session.commit()

    # send welcome email
    job = delay.queue(5)
    queued_task = Task(id=job.id, name="Wait", description="Hold up", user=user)
    db.session.add(queued_task)
    db.session.commit()
    return jsonify({"task": "started", "task_id": queued_task.id})


@sandbox_bp.route('/sandbox-error', methods=['GET'])
def sandbox_error():
    logger.info("[Web] Hit sandbox endpoint")

    user = User(email=str(uuid.uuid4()))
    db.session.add(user)
    db.session.commit()

    job = delay_error.queue(5)
    queued_task = Task(id=job.id, name="Wait", description="Hold up", user=user)
    db.session.add(queued_task)
    db.session.commit()

    return jsonify({"task": "started", "task_id": queued_task.id})
