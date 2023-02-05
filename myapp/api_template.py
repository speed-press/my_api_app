import logging
from uuid import uuid4
from typing import Any, Union

from flask_restx import Namespace, Resource
from flask import request, g, current_app as app, Response

from core.parsers import keyParser
from core.decorators import require_app_key
from core.db import get_db
from core._logging.eLogger import endpoint_logger
from core.format_utils import clean_data
from myapp.response_utils import format_response, response


# You can introduce logging at any section by calling the specific 
# logger you want. For example, we call endpoint below and at any point
# you can call logger.info("message")

logger = logging.getLogger('endpoint')



class ApiTemplate():
    """ Takes in a settings dictionary to create a custom endpoint 
    within the api namespace. A custom function can be provided to 
    override the default/simple input  (arg) --> query --> result.
    """
    
    def __init__(self,api: Namespace, settings: dict[str, Any]):
        # A sample settings configuration is provided in myapp.store.endpoints

        # This section has been simplified for the sake of this example
        # There are better ways to handle the loading of these settings

        self.settings = settings
        self.api = api
        self.query = ''
        self.custom_functions = None
        self.query = None
        self.model = None
        self.parser = None
        self.methods = 'GET'
        self.route = settings['route']
        # Parent is a way to group endpoints. Primarily for logging/analytics
        self.app = f"{settings['parent_name']}"
        self.endpoint = f"{settings['name']}"
        self.procedure = None
        self.marshal = settings['marshal']
        
        if 'methods' in settings:
            self.methods = settings['methods'].upper()
        
        # Custom functions are used when you want to run more complex queries
        # or when the request may require multiple queries, joins, transforms, etc
        if 'custom_functions' in settings:
            self.custom_functions = settings['custom_functions']
        
        # Stored procedures in the settings will take precedence over custom functions
        # and will execute using the MySql method for stored procedures. You can introduce
        # different methods if necessary in core.db
        if 'procedure' in settings:
            self.procedure = settings['procedure']
        # Arguments defined in the settings are used to parse the request
        if 'args' in settings:
            self.parser = keyParser(settings['args'])
        # Query 
        if 'query' in settings:
            self.query = settings['query']
        if 'model' in settings:
            self.model = settings['model']
    
    @property
    def parser(self):
        parser = keyParser(self.settings['args'])
        return parser

    # Request marshaling ensures that the response is formatted correctly. 
    # The template doesn't include marshaling but has examples.
    @property
    def marshal(self):
        mod = self.model
        return self.api.marshal_with(mod) if mod is not None else lambda x: x
    
    # Set global defaults for each request. g is a flask global object that can 
    # be used to store data for the duration of the request. (within the req context)
    @app.before_request
    def set_id():
        g.req_id = uuid4()
        g.query_count = 0
        g.results = 0
        g.path = ""
        g.parent = ""
        g.endpoint = ""
        g.app = ""
        
    ####################################################################
    # We initiate the database object here. Alternatively, you can
    # store the database connectivity in g (flask g)
    ####################################################################
        
    def initiate_endpoint(self):
        """
            @require_app_key
            Require app key is one way to require a user to authenticate
            using an app key. How you manage that is up to you, but this
            library provides a very VERY simple way to do it. You can
            also require the api key using the keyparser. I would recommend
            implementing a more robust auth mechanism for production. 
            JWT/Flask-Login etc.
            
            parser.add_argument('api_key', required=True, location='headers')
        """
        
        # Assigning to variable for ease of access in the nested class
        s = self
        
        
        # Setting up the route and callable methods for the endpoint from settings
        @s.api.route(self.route, methods=[self.methods])
        class Endpoint(Resource):
            
            @property
            def parent(self):
                return s.app
            
            # We intantiate all methods even if they are not used. 
            # Very small overhead, but makes the deployment from config simpler.
            # You can re-write this to dynamically instantiate these methods, but
            # I found it not worth the trouble.

            @require_app_key
            @endpoint_logger
            def get(self):
                
                return process_request(settings=s, request=request)
            
            @require_app_key
            @endpoint_logger
            def post(self):
                
                return process_request(settings=s, request=request)
            
            @require_app_key
            @endpoint_logger
            def delete(self):
                
                return process_request(settings=s, request=request)
            
            @require_app_key
            @endpoint_logger
            def update(self):
                
                return process_request(settings=s, request=request)
            
        return Endpoint

def process_request(settings, request):
    "Function to process each request type"
    
    g.request = request
    method = request.method
    
    # Validate the method used
    if method not in settings.methods: return method_response(method)
        
    # Retrieve DB object
    db = get_db()
    
    # Parse args
    parser = settings.parser

    args = parser.parse_args(req=request)
    
    args = clean_data(args)
    
    # Run a stored procedure or custom function if one is supplied
    # Stored procedure takes precendence
    
    
    if settings.procedure:
        result = db.execute(format_args=args, procedure_name=settings.procedure)
    elif settings.custom_functions or request.method != 'GET':
        result = settings.custom_functions[method](args)
    else:
        # Assumes simple select query is used. 
        # Update, Insert, etc requires custom function.
        result = db.execute(query=settings.query, format_args=args)
    
    if request.method == 'GET':
        return format_response(result)   
    else:
        return result
        
def method_response(method):
    
    message = f"Endpoint does not support the the method {method}."
    
    return response(message, 400)
