import logging

from flask_restx import Namespace, Resource, fields

from mylogging import elog, endpoint_logger
from myapp.parsers import keyParser
from myapp.decorators import require_app_key
from myapp.db import get_db
from myapp.format_utils import formatResponse

logger = logging.getLogger(__name__)
loggerE = logging.getLogger('endpoint')
loggerD = logging.getLogger('data')
loggers = { "data": loggerD, "endpoint": loggerE, "root": logger}

class ApiTemplate():
    
    """ Takes in a settings dictionary to create a custom endpoint 
    within the api namespace. A custom function can be provided to 
    override the default/simple input  (arg) --> query --> result.

    """
    def __init__(
            self, 
            api: Namespace,
            settings: dict,
            custom_function = None,
            model: fields = None):
    
        self.settings = settings
        self.api = api
        self.queryString = settings['query']
        self.log_path = self.get_log_path()
        self.custom_function = custom_function
        
        if 'method' in settings:
            self.method = settings['method'].upper()
        else:
            self.method = 'GET'
        if 'model' in settings:
                self.model = settings['model']
        else:
            self.model = None

    def get_parser(self):
        parser = keyParser(self.settings['args'])
        return parser
        
    def get_log_path(self):
        settings = self.settings
        return "{}.{}".format(settings['parent'], settings['name'])
        
    def send_query(self, queryArgs):
        data = self.db.rowsToList(self.db.query(self.queryString, queryArgs))
        return data

    def get_marshal(self):
        """ Response marshalling 
        https://flask-restx.readthedocs.io/en/latest/marshalling.html
        """
        mod = self.model
        return self.api.marshal_with(mod) if mod is not None else lambda x: x
    
    ####################################################################
    # We initiate the database object here. Alternatively, you can
    # store the database connectivity in g (flask g)
    ####################################################################

    def load_endpoint(self):
        config = self
        e_name = f"{config.settings['parent']}.{config.settings['name']}"
        parser = config.get_parser()
        route = config.settings['route']
        @config.api.route(route, methods=['GET'])
        class Endpoint(Resource):

            """
            @require_app_key
            Require app key is one way to require a user to authenticate
            using an app key. How you manage that is up to you, but this
            library provides a very VERY simple way to do it. You can
            also require the api key using the keyparser.
            
            parser.add_argument('api_key', required=True, location='headers')
            """
            #@require_app_key
            @elog(e_name=e_name, loggers=loggers)
            def get(self):
                """ 
                get_db()
                For testing purposes, get_db has been commented out as
                most will not have a pyodbc connection requirement.
                """
                args = parser.parse_args()
                args_repr = [f"{k}={v!r}" for k, v in args.items()]
                #args_repr = repr(args)
                loggerE.debug(f"Endpoint {e_name} called with args {args_repr}")
                #db = get_db()
                """
                Custom functions must remember to access the global g.db
                """
                if config.custom_function:
                    data = config.custom_function(args=args)
                else:
                    data = db.query(kwargs)
                return formatResponse(data)

        return Endpoint