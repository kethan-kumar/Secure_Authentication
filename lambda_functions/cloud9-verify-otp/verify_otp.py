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

    try:
        user_mail = json.loads(event['body'])['emailid']
        user_otp = json.loads(event['body'])['user_otp']

        client = boto3.resource('dynamodb', region_name=region_name, aws_access_key_id=aws_access_key_id,
                                aws_secret_access_key=aws_secret_access_key, aws_session_token=aws_session_token)
        table = client.Table('cloud9_users')

        response = table.get_item(
            Key={
                'emailid': user_mail
            }
        )
        dyno_otp = response['Item']['user_otp']

        if user_otp == dyno_otp:
            return {
                "statusCode": 200,
                "body": json.dumps({'status': 'success'}),
                "headers": {
                    "content-type": "application/json"
                }
            }
    except:
        return {
            "statusCode": 404,
            "body": json.dumps({'status': 'failure', 'response': 'OTP not found'}),
            "headers": {
                "content-type": "application/json"
            }
        }

    return {
        "statusCode": 401,
        "body": json.dumps({'status': 'failure', 'response': 'Unauthorized'}),
        "headers": {
            "content-type": "application/json"
        }
    }
