"""Flask models used for response marshalling 
https://flask-restx.readthedocs.io/en/latest/marshalling.html"""

from flask_restx import fields


################### Model ######################
nested = {}
nested['nestedField1'] = fields.String(attribute='nestedfield')
nested['nestedField2'] = fields.String(attribute='nestedfield2')

sample_model = {}
sample_model['firstname'] = fields.String(attribute='_name')
sample_model['lastname'] = fields.String(attribute='lastname')
sample_model['nesteddata'] = fields.List(fields.Nested(nested))
