import configparser
import json

import boto3


def lambda_handler(event, context):
    configuration = configparser.ConfigParser()
    configuration.read('credentials.ini')

    region_name = configuration.get('default', "region_name")
    aws_access_key_id = configuration.get('default', "aws_access_key_id")
    aws_secret_access_key = configuration.get('default', "aws_secret_access_key")
    aws_session_token = configuration.get('default', "aws_session_token")

    user_mail = json.loads(event['body'])['emailid']
    user_password = json.loads(event['body'])['password']

    # Retrieve secret
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        aws_session_token=aws_session_token
    )

    try:
        get_secret_value_response = client.get_secret_value(SecretId=user_mail)
    except:
        return {
            "statusCode": 404,
            "body": json.dumps({'status': 'failure'}),
            "headers": {
                "content-type": "application/json"
            }
        }

    if get_secret_value_response:
        response = json.loads(get_secret_value_response.get('SecretString'))

        return {
            "statusCode": 200,
            "body": json.dumps({'status': 'success', 'response': response}),
            "headers": {
                "content-type": "application/json"
            }
        }
