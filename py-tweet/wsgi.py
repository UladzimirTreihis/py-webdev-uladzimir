import sys

# The "/home/webdevUladzimir" below specifies your home
# directory -- the rest should be the directory you uploaded your Flask
# code to underneath the home directory.  So if you just ran
# "git clone git@github.com/myusername/myproject.git"
# ...or uploaded files to the directory "myproject", then you should
# specify "/home/webdevUladzimir/myproject"
path = '/home/webdevUladzimir/py-webdev-uladzimir/py-tweet'
if path not in sys.path:
    sys.path.append(path)

from app import create_app, db
from flask_migrate import Migrate
from app.models import Role, User, Post, Comment

application = create_app('production')
migrate = Migrate(application, db)
application.app_context().push()
db.create_all()

if not db.session.execute(db.select(User)).scalar():

    from add_data import add_data

    with application.app_context():
        add_data(db, Role, User, Post, Comment)