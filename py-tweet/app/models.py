from . import db, login_manager
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask import url_for


class Role(db.Model):
    __tablename__ = 'roles'
    extend_existing=True
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(30), nullable=False)

    users = db.relationship('User', backref='role')

    def __repr__(self) -> str:
        return "Role %r" % self.role


class Follow(db.Model):
    __tablename__ = 'follows'
    follower_id = db.Column(db.Integer, db.ForeignKey('users.id'),
    primary_key=True)
    followed_id = db.Column(db.Integer, db.ForeignKey('users.id'),
    primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    name = db.Column(db.String(64))
    surname = db.Column(db.String(64))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(128))
    comments = db.relationship('Comment', backref='user', lazy='dynamic')

    posts = db.relationship('Post', backref='user', lazy='dynamic')
    followed = db.relationship('Follow',
        foreign_keys=[Follow.follower_id],
        backref=db.backref('follower', lazy='joined'),
        lazy='dynamic',
        cascade='all, delete-orphan')
    followers = db.relationship('Follow',
        foreign_keys=[Follow.followed_id],
        backref=db.backref('followed', lazy='joined'),
        lazy='dynamic',
        cascade='all, delete-orphan')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self) -> str:
        return '<User %r>' % self.username

    def as_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}

    def is_following(self, user):
        if user.id is None:
            return False
        return self.followed.filter_by(
            followed_id=user.id).first() is not None

    def is_followed_by(self, user):
        if user.id is None:
            return False
        return self.followers.filter_by(
            follower_id=user.id).first() is not None

    def follow(self, user):
        if not self.is_following(user):
            f = Follow(follower=self, followed=user)
            db.session.add(f)

    def unfollow(self, user):
        f = self.followed.filter_by(followed_id=user.id).first()
        if f:
            db.session.delete(f)

    def to_json(self):
        json_user = {
            'url': url_for('api.get_user', id=self.id),
            'username': self.username,
            'name': self.name,
            'surname': self.surname,
            'email': self.email,
            # 'role_url': url_for('api.get_role', id=self.role_id),
            # 'posts_url': url_for('api.get_user_posts', id=self.id),
            # 'followed_posts_url': url_for('api.get_user_followed_posts',
            #                               id=self.id),
            'post_count': self.posts.count()
        }
        return json_user
            


class Post(db.Model):
    __tablename__ = 'posts'
    extend_existing=True
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(30), nullable=False)
    created_time = db.Column(db.DateTime, nullable=False, default=datetime.now())
    updated_time = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id')) 
    comments = db.relationship('Comment', backref='post', lazy='dynamic')

    def __repr__(self) -> str:
        return "Content %r" % self.content 

    def as_dict(self):
       return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}

    def to_json(self):
        json_post = {
            'url': url_for('api.get_post', id=self.id),
            'content': self.content,
            'created_time': self.created_time,
            'updated_time': self.updated_time,
            'user_url': url_for('api.get_user', id=self.user_id),
        }
        return json_post


@login_manager.user_loader
def load_user(user_id):
    return db.session.execute(db.select(User).where(User.id==int(user_id))).scalar()


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))

    def to_json(self):
        json_comment = {
            'url': url_for('api.get_comment', id=self.id),
            'post_url': url_for('api.get_post', id=self.post_id),
            'body': self.body,
            'timestamp': self.timestamp,
            'user_url': url_for('api.get_user', id=self.user_id),
        }
        return json_comment