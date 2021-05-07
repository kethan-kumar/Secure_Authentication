import json

import requests

from configuration import config

URL_SECTION_NAME = "loan"
LOAN_URL = config.readConfig(URL_SECTION_NAME, 'loan_update')
LOAN_FILE_UPLOAD_URL = config.readConfig(URL_SECTION_NAME, 'uploads')

TOKEN = config.readConfig("token")


def appLoan(userData):
    dataToSend = json.loads(json.dumps({
        "emailid": userData["emailid"],
        "send_mail": "true",
        "update_user_loan": "true",
        "username": userData["name"],
        "application_status": "submitted",
        "loan_amount": userData["amount"],
        "loan_tenure_in_days": userData["time"],
        "dob": userData["dob"],
        "annual_income": userData["income"]
    }))

    file = userData["loanFile"]
    file_data = file.read()

    file_response = requests.post(LOAN_FILE_UPLOAD_URL, file_data,
                                  headers={"Content-Type": "application/pdf", "emailid": userData["emailid"],
                                           "cloud9_token": TOKEN})

    print(file_response.text)
    response = requests.post(LOAN_URL, data=json.dumps(dataToSend), headers={"cloud9_token": TOKEN})
    if (response.status_code == 200):
        return True
    else:
        return False


def trackLoan(emailid):
    userData = json.loads(json.dumps({
        "emailid": emailid,
        "send_mail": "false",
        "update_user_loan": "false",
    }))

    response = requests.post(LOAN_URL, data=json.dumps(userData), headers={"cloud9_token": TOKEN})
    print(response.text)
    if (response.status_code == 200):
        response = json.loads(response.text)
        print(response)

        application_data = response["loan_status"]
        return application_data["application_status"]
    else:
        return False
