q_customer_info1 = """
    SELECT customer_id, customer_firstname, customerr_lastname, 
    customer_join_date, customer_address1, customer_address2, 
    customer_state, customer_zip 
    FROM `customer`.`customer_info1 
    WHERE customer_id = '{customer_id}'
    """

