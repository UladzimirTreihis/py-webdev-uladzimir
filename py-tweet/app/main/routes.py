from flask import json
from .. import db
from ..models import User, Post
from . import main
from flask import render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
from ..decorators import admin_required, check_role
from .forms import AddPostForm
from datetime import datetime


# Index route: 
# returns all posts sorted by data (DESC)
@main.route("/", methods=['GET', 'POST'])
@main.route("/index", methods=['GET', 'POST'])
def index():
    form=AddPostForm()
    if request.method == 'POST':
        post = Post(
            content=form.content.data,
            created_time=datetime.now(),
            user_id=current_user.id
        )
        db.session.add(post)
        db.session.commit()
        return redirect(url_for("main.index"))

    if request.method == 'GET':
        posts = db.session.execute(
            db.select(Post)
        ).scalars()
        posts_dumps = json.dumps([post.as_dict() for post in posts])
        #return posts_dumps
        return render_template("index.html", form=form, posts=json.loads(posts_dumps))

    
@main.route('/user/<username>')
def user(username):
    user = db.session.execute(db.select(User).where(User.username==username)).scalar()
    # select all posts that belong to this user, use scalars().
    # posts =  
    # create posts_dumps and user_dumps
    # pass json objects to the template
    # posts = db.session.execute(db.select(Post).join(Follow, Follow.followed_id==Post.user_id).where(Follow.follower_id==5)).scalars()
    posts = db.session.execute(db.select(Post).where(Post.user==user)).scalars()
    posts_dumps = json.dumps([post.as_dict() for post in posts])
    user_dumps = json.dumps(user.as_dict())
    return render_template('user.html', user=json.loads(user_dumps), posts=json.loads(posts_dumps))


@main.route('/follow/<username>')
@login_required
def follow(username):
    user = db.session.execute(db.select(User).where(User.username==username)).scalar()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('main.index'))
    if current_user.is_following(user):
        flash('You are already following this user.')
        return redirect(url_for('main.user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash('You are now following %s.' % username)
    return redirect(url_for('main.user', username=username))


@main.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = db.session.execute(db.select(User).where(User.username==username)).scalar()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('main.index'))
    if not current_user.is_following(user):
        flash('You are not following this user.')
        return redirect(url_for('main.user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash('You are not following %s anymore.' % username)
    return redirect(url_for('main.user', username=username))


@main.route("/admin", methods=['GET', 'POST'])
@login_required
@admin_required
def admin():    
    return "Hello, Admin"


@main.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@main.app_errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500