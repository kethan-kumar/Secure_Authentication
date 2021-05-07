import configparser
import json
import uuid

import boto3


def lambda_handler(event, context):
    configuration = configparser.ConfigParser()
    configuration.read('credentials.ini')

    region_name = configuration.get('default', "region_name")
    aws_access_key_id = configuration.get('default', "aws_access_key_id")
    aws_secret_access_key = configuration.get('default', "aws_secret_access_key")
    aws_session_token = configuration.get('default', "aws_session_token")

    description = configuration.get("ssm", "Description")
    kms_key_id = configuration.get("ssm", "KmsKeyId")

    user_mail = json.loads(event['body'])['emailid']
    user_password = json.loads(event['body'])['password']
    user_uuid = str(uuid.uuid4())

    try:
        # Create secret
        ssm = boto3.client('secretsmanager')
        response = ssm.create_secret(
            Description=description,
            Name=user_mail,
            SecretString=json.dumps(
                {"emailid": str(user_mail), "password": str(user_password), "emailid_uuid": str(user_uuid)}),
            KmsKeyId=kms_key_id
        )

        # Retrieve secret
        session = boto3.session.Session()
        client = session.client(
            service_name='secretsmanager',
            region_name=region_name,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            aws_session_token=aws_session_token
        )

        get_secret_value_response = client.get_secret_value(SecretId=str(user_mail))

        salt = json.loads(get_secret_value_response.get('SecretString'))

        save_in_dynamo(event, user_mail, region_name, aws_access_key_id, aws_secret_access_key, aws_session_token)

        return {
            "statusCode": 200,
            "body": json.dumps({'status': 'success', 'salt': salt}),
            "headers": {
                "content-type": "application/json"
            }
        }
    except:
        return {
            "statusCode": 404,
            "body": json.dumps({'status': 'failure'}),
            "headers": {
                "content-type": "application/json"
            }
        }


def save_in_dynamo(event, user_mail, region_name, aws_access_key_id, aws_secret_access_key, aws_session_token):
    client = boto3.resource('dynamodb', region_name=region_name, aws_access_key_id=aws_access_key_id,
                            aws_secret_access_key=aws_secret_access_key, aws_session_token=aws_session_token)
    table = client.Table('cloud9_users')

    try:
        table.put_item(Item={
            'emailid': json.loads(event['body'])['emailid'],
            'username': json.loads(event['body'])['username'],
            'password': json.loads(event['body'])['password'],
            'mobile': json.loads(event['body'])['mobile'],
            'account_number': json.loads(event['body'])['account_number'],
            'user_otp': '-1'
        })
    except:
        return {
            "statusCode": 404,
            "body": json.dumps({'status': 'failure'}),
            "headers": {
                "content-type": "application/json"
            }
        }
