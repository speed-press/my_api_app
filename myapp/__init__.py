import logging

from flask_restx import Api
from flask import Blueprint

from .store.api import api as store_ns


logger = logging.getLogger(__name__)

blueprint = Blueprint('v1', __name__)
api = Api(blueprint)
api.add_namespace(store_ns, path='/')

@api.errorhandler
def server_error(err):
    """
    Handle error during request.
    """
    logger.exception('An error occurred during a request.')
    logger.exception(err)
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(err), 500

