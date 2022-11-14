q_customer_orders = """
    SELECT corder_no, order_date, customer_id, product_code, 
    product_name, product_price, quantity 
    FROM `sales`.`orders` 
    WHERE customer_id = {customer_id} AND order_date 
    BETWEEN '{date_start}' AND '{date_end}'
    """
