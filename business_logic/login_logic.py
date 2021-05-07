import json
import os
from os import path

import requests

from business_logic import crypto_logic
from configuration import config

URL_SECTION_NAME = "login"

VALIDATE_USER_URL = config.readConfig(URL_SECTION_NAME, 'validate_user')
VALIDATE_OTP_URL = config.readConfig(URL_SECTION_NAME, 'validate_otp')
SEND_OTP_URL = config.readConfig(URL_SECTION_NAME, 'send_otp')

TOKEN = config.readConfig("token")
HOME_PATH = os.path.expanduser('~')


def getLocalSeed(userId):
    seedName = userId + "_seed.enc"
    SEED_LOCATION = os.path.join(HOME_PATH, seedName)
    print(SEED_LOCATION)
    if (path.exists(SEED_LOCATION)):
        temp = open(SEED_LOCATION, "r")
        data = temp.read()
        temp.close()
        return data
    return False


def isUserValid(userId, password, otp=""):
    userData = json.dumps({
        "emailid": userId,
        "password": password
    })
    url = VALIDATE_USER_URL
    res = requests.post(url, data=userData, headers={"cloud9_token": TOKEN})
    if (res.status_code == 200):
        resData = json.loads(res.text)["response"]
        print(resData)
        print(res)
        isSeedPresent = getLocalSeed(userId)
        if (isSeedPresent):
            print("Local Seed Found")
            try:
                decryptedSeed = crypto_logic.decrypt(isSeedPresent, password)
            except:
                responseToReturn = {
                    "isCorrect": False,
                    "message": "Password Wrong"
                }
                return responseToReturn
            print(decryptedSeed)
            responseToReturn = {
                "isCorrect": True,
                "message": ""
            }
            return responseToReturn
        else:
            print("Seed Not Found")
            if (otp):
                print("Inside OTP:" + str(otp))
                url = VALIDATE_OTP_URL
                userData = json.dumps({
                    "emailid": userId,
                    "user_otp": otp
                })
                res = requests.post(url, data=userData, headers={"cloud9_token": TOKEN})
                print(json.loads(res.text))
                if (res.status_code == 200):
                    is_accessible = os.access(HOME_PATH, os.F_OK)  # Check if you have access, this should be a path
                    if is_accessible == False:  # If you don't, create the path
                        os.makedirs(HOME_PATH)
                    os.chdir(HOME_PATH)  # Check now if the path exist

                    seedName = userId + "_seed.enc"
                    SEED_LOCATION = os.path.join(HOME_PATH, seedName)

                    f = open(SEED_LOCATION, "w")

                    if (password == str(resData["password"])):
                        encrptedSeed = crypto_logic.encrypt(str(resData["emailid_uuid"]), str(resData["password"]))
                        f.write(encrptedSeed.decode())
                        f.close()
                        responseToReturn = {
                            "isCorrect": True,
                            "message": ""
                        }
                        return responseToReturn
                else:
                    responseToReturn = {
                        "isCorrect": False,
                        "message": "OTP is Wrong"
                    }
                    return responseToReturn
            else:
                url = SEND_OTP_URL
                requests.post(url, data=userData, headers={"cloud9_token": TOKEN})
                responseToReturn = {
                    "isCorrect": False,
                    "message": "OTP"
                }
                return responseToReturn

    responseToReturn = {
        "isCorrect": False,
        "message": "invalid User"
    }
    return responseToReturn
