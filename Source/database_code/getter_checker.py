# Create an instance of the CustomerDataInterface class
from database_code.customer_data_interface import CustomerDataInterface

customer_data_interface = CustomerDataInterface()

# Specify the customer ID
customer_id = 'nic@secretsmokestack.com'

# Call the get_customer_data method
customer_data = customer_data_interface.get_customer_data(customer_id)

# Print the customer data
print(customer_data)
