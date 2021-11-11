from functools import wraps
from flask import redirect, session
import urllib.parse
import requests

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/alogin")
        return f(*args, **kwargs)
    return decorated_function