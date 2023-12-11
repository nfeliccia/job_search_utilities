import csv

import boto3

from database_code.customer_data_interface import ReferenceValues


# Function to add/update customers in DynamoDB
def add_customers_to_dynamodb(file_path):
    dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
    table = dynamodb.Table('customer_data')

    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            row: dict
            customer_id = row['email']  # Assuming email as a unique identifier

            # Check if the record already exists
            response = table.get_item(Key={'customer_id': customer_id})
            if 'Item' in response:
                print(f"Skipping existing customer: {customer_id}")
                continue  # Skip this record and continue with the next

            # Convert search_terms from comma-separated string to list
            search_terms_str = row.get('search_terms', '')
            search_terms_list = search_terms_str.split(',')
            # Convert search_terms from comma-separated string to list

            # Create a ReferenceValues instance
            reference_values = ReferenceValues(
                    first_name=row['first_name'],
                    last_name=row['last_name'],
                    current_resume_path=row.get('current_resume_path', None),
                    email=row['email'],
                    linkedin_url=row['linkedin_url'],
                    phone=row['phone'],
                    location=row['location'],
                    current_company=row['current_company'],
                    current_title=row['current_title'],
                    address=row['address'],
                    city=row['city'],
                    state=row['state'],
                    zip=row['zip'],
                    search_terms=search_terms_list
            )

            # Update DynamoDB
            response = table.put_item(
                    Item={
                        'customer_id': row['email'],  # Assuming email as a unique identifier
                        **vars(reference_values)
                    }
            )
            print(f"Added/Updated customer: {row['email']}")
            return (response)


# Example usage
csv_file_path = r'F:\job_search_utilities\Data\new_customers.csv'
add_customers_to_dynamodb(csv_file_path)
