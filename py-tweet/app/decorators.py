from functools import wraps
from flask import abort
from flask_login import current_user
from . import db
from .models import Role

def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            current_role = current_user.role
            if current_role.role != role:
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def admin_required(f):
    return role_required('Admin')(f)


def check_role(role):
    current_role = current_user.role
    if current_role.role != role:
        abort(403)
    return True