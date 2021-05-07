import base64
import configparser
import logging

import boto3
from botocore.exceptions import ClientError


def lambda_handler(event, context):
    configuration = configparser.ConfigParser()
    configuration.read('credentials.ini')

    region_name = configuration.get('default', "region_name")
    aws_access_key_id = configuration.get('default', "aws_access_key_id")
    aws_secret_access_key = configuration.get('default', "aws_secret_access_key")
    aws_session_token = configuration.get('default', "aws_session_token")

    s3_file_path = configuration.get('s3', "s3_file_path")
    bucket = configuration.get('s3', "s3_bucket_name")

    # user_mail = event['emailid']
    user_mail = 'user4@example.com'
    file_path = upload_pdf(event, bucket, s3_file_path, user_mail)

    return {
        'statusCode': 200,
        'body': {
            'file_path': file_path
        }
    }


def upload_pdf(event, bucket, s3_file_path, user_mail):
    BUCKET_NAME = bucket
    file_content = base64.b64decode(event['content'])
    file_path = s3_file_path + '/' + user_mail + '.pdf'
    s3 = boto3.client('s3')
    try:
        s3_response = s3.put_object(Bucket=BUCKET_NAME, Key=file_path, Body=file_content, ContentType='application/pdf')
    except Exception as e:
        raise IOError(e)
    return file_path


def upload_file(file_name, bucket, object_name=None):
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True


def download_files(file_name, bucket):
    s3 = boto3.client('s3')
    s3.download_file(bucket, file_name, file_name)

# def get_user_details(region_name, aws_access_key_id, aws_secret_access_key, aws_session_token, user_mail):
#     client = boto3.resource('dynamodb', region_name=region_name, aws_access_key_id=aws_access_key_id, 
#                     aws_secret_access_key=aws_secret_access_key, aws_session_token=aws_session_token)
#     table = client.Table('cloud9_users')

#     response = table.get_item(
#         Key={
#             'emailid': user_mail
#         }
#     )
#     username = response['Item']['emailid']
