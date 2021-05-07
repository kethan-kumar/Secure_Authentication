def lambda_handler(event, context):
    authorizer_token = 'U29tZVNlY3VyZVRva2VuIzEyMzQ='
    cloud9_token = str(event['authorizationToken'])

    if (cloud9_token == authorizer_token):
        return {
            "principalId": "232304625378",
            "policyDocument": {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Action": "execute-api:Invoke",
                        "Effect": "Allow",
                        "Resource": "arn:aws:execute-api:us-east-1:232304625378:jpl6e643r3/*"
                    }
                ]
            },
            "context": {
                "stringKey": "value",
                "numberKey": "1",
                "booleanKey": "true"
            },
            "usageIdentifierKey": "fUVPKrSBQI6TMMnB8uDUm3qFfqsXy75I63kYnbIN"
        }
    return {
        'statusCode': 401,
        'body': 'Unauthorized'
    }
