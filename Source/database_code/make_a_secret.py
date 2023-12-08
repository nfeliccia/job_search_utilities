import json
import logging

import boto3


def store_secret(company_name: str, user_id: str, password: str):
    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(service_name='secretsmanager', region_name='us-east-2')

    secret_name = f"{company_name}_{user_id}"
    secret_value = json.dumps({secret_name: password})  # Store as a key-value pair
    description = f"{secret_name} log in for job search utilities"

    try:
        # Try to create the secret
        client.create_secret(
                Name=secret_name,
                Description=description,
                SecretString=secret_value,
                KmsKeyId='alias/aws/secretsmanager',  # Default encryption key
        )
    except client.exceptions.ResourceExistsException:
        # If the secret already exists, update it
        client.update_secret(
                SecretId=secret_name,
                SecretString=secret_value
        )
    except Exception as e:
        logging.error(f"Failed to create or update secret: {e}")
