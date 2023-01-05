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


logger = logging.getLogger('endpoint')
loggerP = logging.getLogger('performance')
loggerD = logging.getLogger('data')

class ApiTemplate():
    """ Takes in a settings dictionary to create a custom endpoint 
    within the api namespace. A custom function can be provided to 
    override the default/simple input  (arg) --> query --> result.
    """
    
    def __init__(self,api: Namespace, settings: dict[str, Any]):

        self.settings = settings
        self.api = api
        self.query = ''
        self.custom_functions = None
        self.query = None
        self.model = None
        self.parser = None
        self.methods = 'GET'
        self.route = settings['route']
        self.app = f"{settings['parent_name']}"
        self.endpoint = f"{settings['name']}"
        self.procedure = None
        
        if 'methods' in settings:
            self.methods = settings['methods'].upper()
        if 'custom_functions' in settings:
            self.custom_functions = settings['custom_functions']
        if 'procedure' in settings:
            self.procedure = settings['procedure']
        if 'args' in settings:
            self.parser = keyParser(settings['args'])
        if 'query' in settings:
            self.query = settings['query']
        if 'model' in settings:
            self.model = settings['model']
  
    def get_parser(self):
        parser = keyParser(self.settings['args'])
        return parser

    def get_marshal(self):
        mod = self.model
        return self.api.marshal_with(mod) if mod is not None else lambda x: x
    
    # Set global defaults
    @app.before_request
    def set_id():
        g.req_id = uuid4()
        g.query_count = 0
        g.results = 0
        g.path = ""
        g.parent = ""
        g.endpoint = ""
        g.app = ""
        
        
    def initiate_endpoint(self):
        # Assigning self to a variable to be accessed 
        s = self
        
        @s.api.route(self.route, methods=[self.methods])
        class Endpoint(Resource):
            
            @property
            def parent(self):
                return s.app
             
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
    args = settings.parser.parse_args(req=request)
    
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
