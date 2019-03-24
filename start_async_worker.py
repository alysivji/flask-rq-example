import sentry_sdk
from sentry_sdk.integrations.rq import RqIntegration

from app.app import create_app
from app.config import IN_PRODUCTION, SENTRY_DSN
from app.extensions import rq
from app.tasks.handlers import retry_failed_job

if IN_PRODUCTION and SENTRY_DSN:
    sentry_sdk.init(SENTRY_DSN, integrations=[RqIntegration()])

app = create_app()
ctx = app.app_context()
ctx.push()

w = rq.get_worker("default", "failed")
w.push_exc_handler(retry_failed_job)
w.work()

# TODO have docker logs go to datadog
