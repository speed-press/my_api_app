from myapp.store.queries import q_customer_info1

customer_info1_config = {
    'name': 'customerInfo',
    'parent': 'customer',
    'route': '/customer/customer-info/',
    'query': q_customer_info1,
    'args':  {
        'name': 'id',
        'required': 'True',
        'location': 'args',
        'type': str,
        'help': 'Customer ID is required',   
    }
}
