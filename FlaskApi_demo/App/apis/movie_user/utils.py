import functools
from flask import request, g
from flask_restful import abort
from App.apis.movie_user.model_utils import get_user
from App.ext import cache


def _verify():
    token = request.args.get("token")
    if not token:
        abort(401, msg="请登录")
    user_id = cache.get(token)
    if not user_id:
        abort(401, msg="user not avaliable")
    user = get_user(user_id)
    if not user:
        abort(401, msg="user not abaliable")
    g.user = user
    g.auth = token


def required(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        _verify()
        ret = func(*args, **kwargs)
        return ret

    return wrapper


def require_permission(permission):
    def require_permission_wrapper(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            _verify()
            if not g.user.check_permission(permission):
                abort(403, msg="user not avaliable")
            ret = func(*args, **kwargs)
            return ret

        return wrapper

    return require_permission_wrapper
