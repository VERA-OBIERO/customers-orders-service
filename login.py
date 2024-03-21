from flask import Flask, abort, redirect, request, session, url_for
from functools import wraps

def login_is_required(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        if args:
            self = args[0]
            if "google_id" not in session:
                return abort(401)
            else:
                return function(*args, **kwargs)
        else:
            return abort(500, "Decorator is not applied to an instance method.")
    return wrapper
