import json
import os

import requests

from business_logic import crypto_logic
from configuration import config

HOME_PATH = os.path.expanduser('~')
URL_SECTION_NAME = "registration"

registrationUrl = config.readConfig(URL_SECTION_NAME, 'register_User')

TOKEN = config.readConfig("token")


def registerUser(userData):
    response = requests.post(registrationUrl, data=json.dumps(userData), headers={"cloud9_token": TOKEN})

    if response.status_code == 200:
        store_seed(userData, json.loads(response.text)["salt"])
        return True
    else:
        return False


def store_seed(userData, response):
    is_accessible = os.access(HOME_PATH, os.F_OK)  # Check if you have access, this should be a path
    if is_accessible == False:  # If you don't, create the path
        os.makedirs(HOME_PATH)
    os.chdir(HOME_PATH)  # Check now if the path exist

    seedName = userData["emailid"] + "_seed.enc"
    SEED_LOCATION = os.path.join(HOME_PATH, seedName)

    f = open(SEED_LOCATION, "w")

    encryptedSeed = crypto_logic.encrypt(str(response["emailid_uuid"]), str(userData["password"]))
    f.write(encryptedSeed.decode())
    f.close()
