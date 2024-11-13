import boto3
import json

class Keys(object):

    def __init__(self, aws_region_name="eu-west-2"):

        self.aws_region_name = aws_region_name
        self.keys = None

    def get_keys(self, aws_secret_name):

        # Create a Secrets Manager client
        session = boto3.session.Session()
        client = session.client(
            service_name="secretsmanager",
            region_name=self.aws_region_name
        )

        try:
            get_secret_value_response = client.get_secret_value(
                SecretId=aws_secret_name
            )
        except Exception as e:

            raise e

        else:
            # Decrypts secret using the associated KMS CMK.
            # Depending on whether the secret is a string or binary, one of these fields will be populated.
            if 'SecretString' in get_secret_value_response:
                secret = get_secret_value_response['SecretString']
                self.keys = json.loads(secret)
            else:
                decoded_binary_secret = base64.b64decode(get_secret_value_response['SecretBinary'])
                self.keys = json.loads(decoded_binary_secret)

        return self.keys
