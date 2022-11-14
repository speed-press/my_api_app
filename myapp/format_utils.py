'''
Utilities to help with formatting the response data
'''
from datetime import datetime
from flask import Response


def formatResponse(data):
    """
    Returns objects as an array if there is data. 
    """
    if len(data) > 0:
        if isinstance(data, list):
            return data, 200
        return [data], 200
    else:
        return Response(response="The request was fulfilled as intended but no result was returned", status=404, mimetype='application/json')

def converter(o):
    """ Formats datetime columns 
    """
    if isinstance(o, datetime.datetime):
        return o.strftime("%Y-%m-%d %H:%M:%S")
    elif isinstance(o, datetime.date):
        return o.strftime("%Y-%m-%d")
    elif isinstance(o, datetime.time):
        return o.strftime("%H:%M:%S")
    else:
        return o.__str__()
 
def toDate(dateString): 
    return datetime.strptime(dateString, "%Y-%m-%d").date()