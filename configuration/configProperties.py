BASE_URL = "https://jpl6e643r3.execute-api.us-east-1.amazonaws.com/cloud9/loan-application"
LOAN_APPLICATION_URLS = {
    "login": {
        "send_otp": "/login/send-otp",
        "validate_otp": "/login/validate-otp",
        "validate_user": "/login/validate-user"
    },
    "registration": {
        "register_User": "/registration/register-user"
    },
    "loan": {
        "loan_update": "/loan/updates",
        "uploads": "/loan/uploads"
    }
}
TOKEN = "U29tZVNlY3VyZVRva2VuIzEyMzQ="


def get(section, key=False):
    if (key):
        url_to_return = BASE_URL + LOAN_APPLICATION_URLS[section][key]
        print(url_to_return)
        return url_to_return
    else:
        return TOKEN
