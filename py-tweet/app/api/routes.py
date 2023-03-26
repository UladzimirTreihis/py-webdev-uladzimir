from . import api
from .. import db
from ..models import Comment, Post, User
from flask import jsonify



@api.route('/comments/')
def get_comments():
    comments = db.session.execute(
        db.select(Comment).order_by(
            Comment.timestamp.desc()
        )
    ).scalars()
    # Note that here we use a method to_json instead of as_dict
    # We should define it in models.py
    return jsonify({
        'comments': [comment.to_json() for comment in comments],
    })


@api.route('/comments/<int:id>')
def get_comment(id):
    comment = db.session.execute(
        db.select(Comment).where(
            Comment.id==id
        )
    ).scalar()
    return jsonify({
        'comment': comment.to_json()
    })


@api.route('/posts/')
def get_posts():
    posts = db.session.execute(
        db.select(Post).order_by(
            Post.created_time.desc()
        )
    ).scalars()
    # Note that here we use a method to_json instead of as_dict
    # We should define it in models.py
    return jsonify({
        'posts': [post.to_json() for post in posts],
    })


@api.route('/posts/<int:id>')
def get_post(id):
    post = db.session.execute(
        db.select(Post).where(
            Post.id==id
        )
    ).scalar()
    return jsonify({
        'post': post.to_json()
    })


@api.route('/users/')
def get_users():
    users = db.session.execute(
        db.select(User).order_by(
            User.id.asc()
        )
    ).scalars()
    # Note that here we use a method to_json instead of as_dict
    # We should define it in models.py
    return jsonify({
        'users': [user.to_json() for user in users],
    })


@api.route('/users/<int:id>')
def get_user(id):
    user = db.session.execute(
        db.select(User).where(
            User.id==id
        )
    ).scalar()
    return jsonify({
        'user': user.to_json()
    })