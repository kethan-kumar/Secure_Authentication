import configparser
import json
import math
import random

import boto3


def sns_handler(event, context):
    configuration = configparser.ConfigParser()
    configuration.read('credentials.ini')

    region_name = configuration.get('default', "region_name")
    aws_access_key_id = configuration.get('default', "aws_access_key_id")
    aws_secret_access_key = configuration.get('default', "aws_secret_access_key")
    aws_session_token = configuration.get('default', "aws_session_token")

    topic_arn = configuration.get('sns', "topic_arn")

    try:
        user_mail = json.loads(event['body'])['emailid']
        send_mail = json.loads(event['body'])['send_mail']
        update_user_loan = json.loads(event['body'])['update_user_loan']

        client = boto3.resource('dynamodb', region_name=region_name, aws_access_key_id=aws_access_key_id,
                                aws_secret_access_key=aws_secret_access_key, aws_session_token=aws_session_token)
        table = client.Table('cloud9-loan-details')

        if update_user_loan == 'true':
            update_loan_details(user_mail, client, table, event)

        response = table.get_item(
            Key={
                'emailid': user_mail
            }
        )

        loan_details = {'username': response['Item']['username'],
                        'application_status': response['Item']['application_status'],
                        'application_number': str(response['Item']['application_number']),
                        'loan_amount': str(response['Item']['loan_amount']),
                        'loan_tenure_in_days': str(response['Item']['loan_tenure_in_days'])}

        if send_mail == 'true':
            send_email(configuration, loan_details, topic_arn)
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
        "body": json.dumps(
            {'status': 'success', 'response': 'Update has been sent to user via mail', 'loan_status': loan_details}),
        "headers": {
            "content-type": "application/json"
        }
    }


def send_email(configuration, loan_details, topic_arn):
    message_greetings = configuration.get('mailconfig', "message_greetings")
    message_body = configuration.get('mailconfig', "message_body")
    message_closing = configuration.get('mailconfig', "message_closing")
    message_subject = configuration.get('mailconfig', "message_subject")
    message_signature = configuration.get('mailconfig', "message_signature")

    client = boto3.client('sns')
    response = response = client.publish(
        TopicArn=topic_arn,
        Message=message_greetings + ' ' + loan_details['username'] + ',\n\n' + message_body
                + '\n\n' + 'Loan Application Details: ' + '\n\n'
                + '\tApplication number: ' + str(loan_details['application_number']) + '\n'
                + '\tApplication status: ' + loan_details['application_status'] + '\n'
                + '\tLoan amount: ' + str(loan_details['loan_amount']) + '\n'
                + '\tLoan tenure (days): ' + str(loan_details['loan_tenure_in_days'])
                + '\n\n'
                + message_closing + ',\n' + message_signature,
        Subject=message_subject
    )


def update_loan_details(user_mail, client, table, event):
    username = json.loads(event['body'])['username']
    application_status = json.loads(event['body'])['application_status']
    application_number = str(generate_random_number())
    loan_amount = json.loads(event['body'])['loan_amount']
    loan_tenure_in_days = json.loads(event['body'])['loan_tenure_in_days']
    dob = json.loads(event['body'])['dob']
    annual_income = json.loads(event['body'])['annual_income']

    update_item(user_mail, 'username', username, table)
    update_item(user_mail, 'application_status', application_status, table)
    update_item(user_mail, 'application_number', application_number, table)
    update_item(user_mail, 'loan_amount', loan_amount, table)
    update_item(user_mail, 'loan_tenure_in_days', loan_tenure_in_days, table)
    update_item(user_mail, 'dob', dob, table)
    update_item(user_mail, 'annual_income', annual_income, table)


def update_item(user_mail, attribute_name, attribute_value, table):
    table.update_item(
        Key={
            'emailid': user_mail
        },
        UpdateExpression='SET ' + attribute_name + ' = :val1',
        ExpressionAttributeValues={
            ':val1': attribute_value
        }
    )


# citation: https://geeksforgeeks.com
def generate_random_number():
    random_number = ""
    random_number_digits = "0123456789"
    for i in range(10):
        random_number += random_number_digits[math.floor(random.random() * 9)]
    return random_number
