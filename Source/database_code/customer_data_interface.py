import logging
import tempfile
from dataclasses import dataclass
from pathlib import Path

import boto3
from botocore.exceptions import BotoCoreError, ClientError


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

    def __init__(self, dynamodb=None, s3=None):
        self.dynamodb = dynamodb or boto3.resource('dynamodb', region_name='us-east-2')
        self.s3 = s3 or boto3.client('s3')
        self.data_type_converter = DataTypeConverter()

    def download_resume_from_s3(self, s3_url):
        if not s3_url.startswith('s3://'):
            return Path(s3_url)

        s3_url_parts = s3_url.replace("s3://", "").split("/")
        bucket, key = s3_url_parts[0], "/".join(s3_url_parts[1:])

        with tempfile.NamedTemporaryFile(delete=True, suffix='.docx') as temp_file:
            self.s3.download_file(bucket, key, temp_file.name)
            return Path(temp_file.name)

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
        search_terms = []
        for term_dict in item.get('search_terms'):
            try:
                search_terms.append(term_dict.get('S'))
            except AttributeError:
                logging.warning(f"Failed to convert all search_terms to a list of strings {term_dict}")

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
        except (BotoCoreError, ClientError) as e:
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
            update_expression = "SET " + ", ".join(f"#{k} = :{k}" for k in updates)
            expression_attribute_names = {f"#{k}": k for k in updates}
            expression_attribute_values = {f":{k}": v for k, v in updates.items()}

            table.update_item(
                    Key={'customer_id': customer_id},
                    UpdateExpression=update_expression,
                    ExpressionAttributeNames=expression_attribute_names,
                    ExpressionAttributeValues=expression_attribute_values,
                    ReturnValues="UPDATED_NEW"
            )
        except (BotoCoreError, ClientError) as e:
            logging.error(f"Failed to update customer data: {e}")

    def get_tables(self):
        try:
            return [table.name for table in self.dynamodb.tables.all()]
        except (BotoCoreError, ClientError) as e:
            logging.error(f"Failed to get tables: {e}")
            return []
