import json
import boto3
from botocore.exceptions import ClientError


def get_openai_api_key():
    secret_name = "OPENAI_API_KEY"
    region_name = "us-east-1"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(service_name="secretsmanager", region_name=region_name)

    try:
        # Fetch the secret value
        response = client.get_secret_value(SecretId=secret_name)

        # Decrypt the secret if it is encrypted
        if "SecretString" in response:
            secret = response["SecretString"]
            secret_dict = json.loads(secret)
            return secret_dict["OPENAI_API_KEY"]
        else:
            raise Exception("Secret value not found.")
    except ClientError as e:
        raise Exception(f"Error retrieving secret: {e}")
    
def read_txt_file(filename: str) -> str:
    with open(filename, 'r') as file:
        content = file.read()
    return content
