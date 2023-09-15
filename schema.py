"""
API schema definition.
"""

req_schema = {
    'title': 'Request schema',
    'type': 'object',
    'required': ['schema', 'count'],
    'properties': {
        'schema': {
            'type': 'object',
            'properties': {
                'title': {
                    'type': 'string'
                }
            },
            'required': ['title'],
        },
        'count': {
            'type': 'number',
            'minimum': 1,
            'maximum': 100
        },
        'format': {
            'type': 'string',
            'enum': [
                'json',
                'xml'
            ]
        }
    },
    'additionalProperties': False
}
