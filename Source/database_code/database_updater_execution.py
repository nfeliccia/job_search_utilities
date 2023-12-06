# Create an instance of the CustomerDataInterface class
from database_code.customer_data_interface import CustomerDataInterface


def update_customer_data(customer_id, updates):
    # Create an instance of the CustomerDataInterface class
    customer_data_interface = CustomerDataInterface()

    # Call the update_customer_data method
    customer_data_interface.update_customer_data(customer_id=customer_id, updates=updates)


# Specify the customer ID and the updates
customer_id = 'nic@secretsmokestack.com'
updates = {
    'search_terms': ['"data science"', '"python"', '"machine learning"']
}
update_customer_data(customer_id, updates)
