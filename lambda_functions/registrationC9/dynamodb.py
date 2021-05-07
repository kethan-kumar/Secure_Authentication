import configparser
import json

import boto3


def dynamodb_handler(event, context):
    configuration = configparser.ConfigParser()
    configuration.read('credentials.ini')

    region_name = configuration.get('default', "region_name")
    aws_access_key_id = configuration.get('default', "aws_access_key_id")
    aws_secret_access_key = configuration.get('default', "aws_secret_access_key")
    aws_session_token = configuration.get('default', "aws_session_token")

    client = boto3.resource('dynamodb', region_name=region_name, aws_access_key_id=aws_access_key_id,
                            aws_secret_access_key=aws_secret_access_key, aws_session_token=aws_session_token)
    table = client.Table('cloud9_users')

    table.put_item(Item={
        'emailid': json.loads(event['body'])['emailid'],
        'username': json.loads(event['body'])['username'],
        'password': json.loads(event['body'])['password'],
        'mobile': json.loads(event['body'])['mobile'],
        'account_number': json.loads(event['body'])['account_number']
    })

    return {
        "statusCode": 200,
        "body": json.dumps({'status': 'success', 'event': json.loads(event['body'])['emailid']}),
        "headers": {
            "content-type": "application/json"
        }
    }
