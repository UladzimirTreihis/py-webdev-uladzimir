from app import create_app, db
from flask_migrate import Migrate
from app.models import User, Role, Post, Follow, Comment
import os

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role, Post=Post, Follow=Follow, Comment=Comment)

