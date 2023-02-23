from functools import wraps
from flask import request, abort, g, current_app as app

from .db import  get_db


def get_apiauth_object_by_key(key: str):
    """
    A simplied method for verifying if an api_key provided by the 
    request exist in a security table. Definitely not production quality
    """
    sql = "SELECT key from `store`.`keys` where private_key = ?"
    db = get_db()
    # We can check the result or just reutrn to the conn and check if
    # there is just one row (meaning theres a result)
    with db.conn.cursor() as cur:
        cur.execute(sql, key)
        try:
            cur.fetchone()[0]
            return True
        except: 
            return False

def authorized(key: str):
    """
    Checks for the existence of an api_key before proceeding.
    """
    if key is None:
      return False
    api_key = get_apiauth_object_by_key(key)
    if api_key:
      return True
    return False

def require_app_key(f):
    """
    Wrapper function to apply to endpoints and check for an api_key
    @param f: flask function
    @return: decorator, return the wrapped function or abort json object
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        if authorized(request.headers.get('api_key')):
            return f(*args, **kwargs)
        else:
            abort(401)
    return decorated

