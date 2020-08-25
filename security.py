from functools import wraps

from flask import jsonify
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    get_jwt_claims,
    verify_jwt_in_request,
)


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if "ADMIN" in claims["roles"]:
            return fn(*args, **kwargs)
        else:
            return ({"msg": "This URL can be accessed by only Admins"}), 403

    return wrapper


def manager_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if "MANAGER" in claims["roles"] or "ADMIN" in claims["roles"]:
            return fn(*args, **kwargs)
        else:
            return {"msg": "Either ADMINS or MANAGERS can access this one!"}, 403

    return wrapper


def employee_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if "EMPLOYEE" in claims["roles"]:
            return fn(*args, **kwargs)
        else:
            return (
                {"msg": "Either EMPLOYEES or MANAGER or ADMIN can access this one!"},
                403,
            )

    return wrapper
