""" 
A database object to connect to databases using pyodbc. Generated from
a requirement to
"""
import pyodbc
import json
import re
import logging 

from werkzeug.datastructures import ImmutableDict as iDict
from flask import g, current_app as app

from myapp.format_utils import converter
from definitions import DB_CONFIG, ENVIRONMENT
from myapp.utils import readConfig

logger = logging.getLogger('query')


class DbConnect():
    
    def __init__(self, config_path: str, section: str):
        """ Sets the config based on the input section """ 
        self.config = readConfig(config_path)
        self.section = section

    def buildConnString(self):
        """ 
        Build a connection string from the config file
        """
        config = self.config
        section = self.section

        driver = config.GetVariableBySection(
            section=section, variableName='driver')
        host = config.GetVariableBySection(
            section=section, variableName='host')
        user = config.GetVariableBySection(
            section=section, variableName='user')
        passwd = config.GetVariableBySection(
            section=section, variableName='psw')
        port = config.GetVariableBySection(
            section=section, variableName='port')
        
        dbString =  (
            'Driver=%s;Server=%s;Port=%s;UID=%s;PWD=%s'
            % (driver, host, port, user, passwd))
        return dbString

    def connect(self):
        "Assigns the connection and cursor to self"
        conn = pyodbc.connect(self.buildConnString())
        self.conn = conn

    def _formatQueryString(self, query, format_args = None):
        """
        Formats the query string
        """
        query_string = ""
        
        if format_args == None:
            """ Do nothing if there if no formatting required """
            query_string = query.lower()
        elif isinstance(format_args, list):
            query_string = query.format(*format_args).lower()
            logger.debug('List found in query format args')
        elif isinstance(format_args, (dict, iDict)):
            logger.debug('Dictionary Found in query format args')
            query_string = query.format(**format_args).lower()        
        else:
            logger.debug('Else in query format args')
            query_string = query.format(format_args).lower()
            
        return query_string
    

    def _rowsToList(self, rows):
        """Adds results from query into a list. 
        """
        result = []
        columns = [column[0] for column in self.conn.description]
        for row in rows:
            result.append(dict(zip(columns, [converter(x) for x in row])))
        if len(result) == 1:
            return result[0]
        else:
            return result
 
    def _trimQueryString(self, string, trim_carriage=True):
        """
        Trims query string carriage returns for better logging in 
        case you have it imported using a formatter. You can also add 
        back in carriage returns for keywords only as well.
        """
        if trim_carriage:
            string = ' '.join(string.split()).lower()
        else:
            string = re.sub(' +', ' ', string)
        return string
        
    def query(self, query, format_args=None):
        """ 
        Will query the db with the given sql query and return the result
        """
        if format_args:
            query = self.formatQueryString(query, format_args)
        logger.debug(f'db query: {self._trimQueryString(string=query)}')
        with self.conn.cursor() as cur:
            data = cur.execute(query)
        return data
  
    def queryJson(self, query):
        """
        Queries the database with a json query string (JSON_OBJECT)
        """
        with self.conn.cursor() as cur:
            cur = self.conn.execute(query)
            for data in cur:
                json_obj = json.loads(data[0])
        return json_obj
    
    def commit(self):
        return self.conn.commit()


def get_db():
    if 'db' not in g:
        g.db = DbConnect(DB_CONFIG, f"STORE_{ENVIRONMENT}")
        g.db.connect()
    return g.db

@app.teardown_appcontext
def teardown_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.conn.close()