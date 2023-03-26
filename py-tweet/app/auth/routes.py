from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, login_required, logout_user
from . import auth
from .. import db
from ..models import User, Role
# Make sure now forms.py in auth have the relevant forms
from .forms import LogInForm, RegisterForm
from emails import send_email


@auth.route('/login', methods=['GET', 'POST'])
def login():
    # Invoke the form we imported before
    form = LogInForm()
    if request.method=='POST':
        # Find the user given its email from the form
        user = db.session.execute(db.select(User).where(User.email==form.email.data)).scalar()
        # If all good, login the user using the flask_login.login_user function
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            # Next 3 lines help us redirect the user to 
            # the page they were going before logining in.
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('main.index')
            return redirect(next)
        # This is flashed only if the password is incorrect
        # or user not found
        flash('Invalid email or password.')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method=='POST':
        user_role = db.session.execute(db.select(Role).where(Role.role=="User")).scalar()
        user = User(email=form.email.data,
        username=form.username.data,
        name = form.name.data,
        surname=form.surname.data,
        password=form.password.data,
        role_id=user_role.id)
        db.session.add(user)
        db.session.commit()
        flash('You can now login.')

        # Send email
        send_email(
            form.email.data, 
            "You are successfully registered",
            "mail/welcome_user",
            url=url_for('main.index', _external=True),
            username=form.username.data
            )
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)