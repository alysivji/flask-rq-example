from app.app import create_app
from app.extensions import db, rq  # noqa
from app.models import Task, User  # noqa

# create flask application context
app = create_app()
ctx = app.app_context()
ctx.push()

# configure adapters


# log to console
display_text = "flask+rq Development Shell"
num_char = len(display_text)
print("*" * num_char)
print(display_text)
print("*" * num_char)
