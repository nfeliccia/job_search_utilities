import logging
import unittest
from pathlib import Path
from unittest.mock import patch

import boto3

from database_code.customer_data_interface import CustomerDataInterface, ReferenceValues


class TestCustomerDataInterface(unittest.TestCase):

    def setUp(self):
        self.customer_id = '12345'
        self.mock_item = {
            'current_resume_path': {'S': 'path/to/resume.pdf'},
            'email': {'S': 'john.doe@example.com'},
            'first_name': {'S': 'John'},
            'last_name': {'S': 'Doe'},
            'linkedin_url': {'S': 'linkedin.com/john-doe'},
            'phone': {'S': '+1234567890'},
            'location': {'S': 'New York, NY'},
            'current_company': {'S': 'Acme Inc.'},
            'current_title': {'S': 'Software Engineer'},
            'address': {'S': '123 Main Street'},
            'city': {'S': 'New York'},
            'state': {'S': 'NY'},
            'zip': {'S': '10001'},
            'search_terms': {'L': [{'S': 'python'}, {'S': 'django'}]}
        }
        self.expected_result = ReferenceValues(
                current_resume_path=Path('path/to/resume.pdf'),
                email='john.doe@example.com',
                first_name='John',
                last_name='Doe',
                linkedin_url='linkedin.com/john-doe',
                phone='+1234567890',
                location='New York, NY',
                current_company='Acme Inc.',
                current_title='Software Engineer',
                address='123 Main Street',
                city='New York',
                state='NY',
                zip='10001',
                search_terms=['python', 'django']
        )

    @patch.object(boto3.resource, 'Table')
    @patch.object(logging, 'error')
    def test_get_customer_data_existing_customer(self, mock_error, mock_table):
        mock_table.get_item.return_value = {'Item': self.mock_item}
        customer_data_interface = CustomerDataInterface()
        result = customer_data_interface.get_customer_data(self.customer_id)
        self.assertEqual(result, self.expected_result)
        mock_table.get_item.assert_called_once_with(Key={'customer_id': self.customer_id})
        mock_error.assert_not_called()
