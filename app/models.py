from datetime import datetime

from redis.exceptions import RedisError
from rq.job import Job
from rq.exceptions import NoSuchJobError
from sqlalchemy.ext.declarative import declared_attr

from app.extensions import db, rq


class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime,
        onupdate=db.func.current_timestamp(),
        default=db.func.current_timestamp(),
    )

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    def patch(self, data: dict):
        for key, value in data.items():
            setattr(self, key, value)


class User(BaseModel):
    """User table"""

    def __repr__(self):
        return f"<User: {self.email}>"

    # Attributes
    email = db.Column(db.String(255), index=True, unique=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    middle_name = db.Column(db.String(255))
    password_hash = db.Column(db.String(255))

    # Relationships
    tasks = db.relationship("Task", back_populates="user")


class Task(BaseModel):
    """Task Information Table"""

    def __repr__(self):
        return f"<Task: {self.id}-{self.name}>"

    # Attributes
    id = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(128), index=True)
    description = db.Column(db.String(128))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", name="fk_task_user_id"))
    failed = db.Column(db.Boolean, default=False)
    complete = db.Column(db.Boolean, default=False)

    # Relationships
    user = db.relationship("User", back_populates="tasks")

    def get_rq_job(self):
        try:
            rq_job = Job.fetch(self.id, rq.connection)
        except (RedisError, NoSuchJobError):
            return None
        return rq_job

    def get_progress(self):
        job = self.get_rq_job()
        return job.meta.get("progress", 0) if job is not None else 100
