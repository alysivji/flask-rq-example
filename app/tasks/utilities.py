import logging

from flask import current_app as app  # noqa
from rq import get_current_job

from app.extensions import db
from app.models import Task

logger = logging.getLogger(__name__)


def _set_task_progress(progress):
    job = get_current_job()
    if job:
        job.meta['progress'] = progress
        job.save_meta()

        if progress >= 100:
            task = Task.query.get(job.get_id())
            task.complete = True
            db.session.commit()
