from myapp.store.queries import q_customer_orders

orders_config = {
    'name': 'customerOrders',
    'parent': 'orders',
    'route': '/orders',
    'query': q_customer_orders,
    'args':  [{
        'name': 'customer_id',
        'required': 'True',
        'location': 'args',
        'type': str,
        'help': 'Customer id is required for this query',   
        },
        {
        'name': 'date_start',
        'required': 'False',
        'location': 'args',
        'type': str,
        'help': 'Date format yyyy-mm-dd'
        },
        {
        'name': 'date_end',
        'required': 'False',
        'location': 'args',
        'type': str,
        'help': 'Date format yyyy-mm-dd'
        }]
    }


