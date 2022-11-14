from flask_restx import reqparse

def keyParser(args) -> reqparse.RequestParser:
    """ Adds the arguments defined in the endpoint dictionary objects.
    You can require an api_key in the headers as seen in the samp below
    """
    parser = reqparse.RequestParser()
    #parser.add_argument('api_key', required=True, location='headers')
    if isinstance(args, list):
        for arg in args:
            parser.add_argument(**arg)
    elif isinstance(args, dict):
        parser.add_argument(**args)
    else:
        raise('Keyparser only works with list of dictionary objects')
    return parser
