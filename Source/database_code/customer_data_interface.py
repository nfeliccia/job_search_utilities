import logging
import tempfile
from dataclasses import dataclass
from pathlib import Path

import boto3
import botocore


@dataclass
class ReferenceValues:
    address: str
    city: str
    current_company: str
    current_resume_path: str
    current_title: str
    email: str
    first_name: str
    last_name: str
    linkedin_url: str
    location: str
    phone: str
    search_terms: list
    state: str
    zip: str


class DataTypeConverter:
    mappings = {
        str: 'S',
        int: 'N',
        bool: 'BOOL',
        list: 'L',
        dict: 'M',  # Map type
        bytes: 'B'  # Binary type
    }

    def to_dynamodb(self, value):
        """Converts the given value to DynamoDB data type."""
        if type(value) not in self.mappings.keys():
            raise ValueError(f"Unsupported datatype: {type(value)}")
        if isinstance(value, list):
            return [{'S': item} for item in value]
        else:
            return {self.mappings[type(value)]: value}


class CustomerDataInterface:
    """Class for interacting with a DynamoDB database."""

    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
        self.data_type_converter = DataTypeConverter()

    def download_resume_from_s3(self, s3_url):
        # Check if the path is an S3 URL
        if not s3_url.startswith('s3://'):
            return s3_url  # Return the original path if it's not an S3 URL

        # Parse the S3 URL
        s3_url_parts = s3_url.replace("s3://", "").split("/")
        bucket = s3_url_parts[0]
        key = "/".join(s3_url_parts[1:])

        # Create a temporary file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.docx')
        tfn = temp_file.name
        temp_file.close()  # Close the file handle to avoid resource leaks

        # Download the file from S3
        s3 = boto3.client('s3')
        s3.download_file(bucket, key, tfn)
        temp_file.close()  # Close the file handle to avoid resource leaks
        return tfn

    def dynamodb_to_python(self, item) -> ReferenceValues:
        """
        Converts a DynamoDB item to a ReferenceValues instance.

        Args:
            item: an item retrieved from DynamoDB
        """
        if not isinstance(item, dict):
            logging.error(f"Item is not a dictionary: {item}")
            return ReferenceValues()

        required_keys = ['current_resume_path', 'email', 'first_name', 'last_name', 'linkedin_url', 'phone', 'location',
                         'current_company', 'current_title', 'address', 'city', 'state', 'zip', 'search_terms']
        if not all(key in item for key in required_keys):
            logging.error(f"Item is missing some required keys: {item}")
            return ReferenceValues()

        # Convert search_terms from DynamoDB format to a list of strings
        search_terms = [term_dict.get('S') for term_dict in item.get('search_terms')]  # List comprehension

        rv_a = ReferenceValues(
                address=item.get('address'),
                city=item.get('city'),
                current_company=item.get('current_company'),
                current_resume_path=item.get('current_resume_path'),
                current_title=item.get('current_title'),
                email=item.get('email'),
                first_name=item.get('first_name'),
                last_name=item.get('last_name'),
                linkedin_url=item.get('linkedin_url'),
                location=item.get('location'),
                phone=item.get('phone'),
                search_terms=search_terms,
                state=item.get('state'),
                zip=item.get('zip'),
        )  # Use the converted search_terms list

        return rv_a

    def get_customer_data(self, customer_id: str = None) -> ReferenceValues:
        """
        Retrieves the data for the customer with the given ID.
        Returns a ReferenceValues instance.
        """
        if not customer_id:
            raise ValueError("Customer ID cannot be None")
        try:
            table = self.dynamodb.Table('customer_data')
            response = table.get_item(Key={'customer_id': customer_id})
            item = response['Item']
            item_pythonized = self.dynamodb_to_python(item)

            # Check and download the resume from S3 if necessary
            resume_s3_path = item_pythonized.current_resume_path
            if resume_s3_path.startswith("s3://"):
                item_pythonized.current_resume_path = self.download_resume_from_s3(resume_s3_path)
            else:
                item_pythonized.current_resume_path = Path(resume_s3_path)  # Convert to Path object if not S3 path

            return item_pythonized
        except botocore.exceptions.BotoCoreError as e:
            logging.error(f"Failed to get customer data due to a BotoCoreError: {e}")
        except botocore.exceptions.ClientError as e:
            logging.error(f"Failed to get customer data due to a ClientError: {e}")
        except Exception as e:
            logging.error(f"Failed to get customer data: {e}")

    def update_customer_data(self, customer_id: str = None, updates: dict = None):
        """
        Updates the data for the customer with the given ID.
        The updates parameter is a dictionary where the keys are the attribute names to update
        and the values are the new values for those attributes.
        """
        if not customer_id or not updates:
            raise ValueError("Customer ID and updates cannot be None")
        try:
            table = self.dynamodb.Table('customer_data')
            update_expression = "SET " + ", ".join(f"{k} = :{k}" for k in updates.keys())
            expression_attribute_values = {f":{k}": self.data_type_converter.to_dynamodb(v) for k, v in updates.items()}
            table.update_item(
                    Key={
                        'customer_id': customer_id
                    },
                    UpdateExpression=update_expression,
                    ExpressionAttributeValues=expression_attribute_values,
                    ReturnValues="UPDATED_NEW"
            )
        except Exception as e:
            logging.error(f"Failed to update customer data: {e}")

    def get_tables(self, dump_to_console: bool = True):
        """
        Retrieves the names of all tables in the DynamoDB database.
        If dump_to_console is True, also prints the table names to the console.
        Returns a list of table names.
        """
        try:
            table_names = [table.name for table in self.dynamodb.tables.all()]
            if dump_to_console:
                for table_name in table_names:
                    print(table_name)
            return table_names
        except Exception as e:
            logging.error(f"Failed to get tables: {e}")
