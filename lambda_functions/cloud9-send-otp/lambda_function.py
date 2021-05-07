import configparser
import json
import math
import random

import boto3


def dynamodb_handler(event, context):
    configuration = configparser.ConfigParser()
    configuration.read('credentials.ini')

    region_name = configuration.get('default', "region_name")
    aws_access_key_id = configuration.get('default', "aws_access_key_id")
    aws_secret_access_key = configuration.get('default', "aws_secret_access_key")
    aws_session_token = configuration.get('default', "aws_session_token")

    message_greetings = configuration.get('mailconfig', "message_greetings")
    message_body = configuration.get('mailconfig', "message_body")
    message_closing = configuration.get('mailconfig', "message_closing")
    message_subject = configuration.get('mailconfig', "message_subject")
    message_signature = configuration.get('mailconfig', "message_signature")

    topic_arn = configuration.get('sns', "topic_arn")

    try:
        user_mail = json.loads(event['body'])['emailid']
        user_otp = generate_otp()

        client = boto3.resource('dynamodb', region_name=region_name, aws_access_key_id=aws_access_key_id,
                                aws_secret_access_key=aws_secret_access_key, aws_session_token=aws_session_token)
        table = client.Table('cloud9_users')

        table.update_item(
            Key={
                'emailid': user_mail
            },
            UpdateExpression='SET user_otp = :val1',
            ExpressionAttributeValues={
                ':val1': user_otp
            }
        )

        response = table.get_item(
            Key={
                'emailid': user_mail
            }
        )
        username = response['Item']['username']

        send_email(message_subject, message_greetings, message_body, message_closing, message_signature, user_otp,
                   username, topic_arn)

    except:
        return {
            "statusCode": 404,
            "body": json.dumps({'status': 'failure', 'response': 'User not found'}),
            "headers": {
                "content-type": "application/json"
            }
        }

    return {
        "statusCode": 200,
        "body": json.dumps({'status': 'success', 'response': 'OTP sent to user email id.'}),
        "headers": {
            "content-type": "application/json"
        }
    }


# citation: https://geeksforgeeks.com
def generate_otp():
    otp = ""
    otp_digits = "0123456789"
    for i in range(6):
        otp += otp_digits[math.floor(random.random() * 10)]

    return otp


def send_email(message_subject, message_greetings, message_body, message_closing, message_signature, user_otp, username,
               topic_arn):
    client = boto3.client('sns')
    response = response = client.publish(
        TopicArn=topic_arn,
        Message=message_greetings + ' ' + username + ',\n\n' + message_body + '\n\n' +
                'One Time Password (OTP): ' + user_otp + '\n\n' + message_closing + ',\n' + message_signature,
        Subject=message_subject
    )
