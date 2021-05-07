'''
https://nitratine.net/blog/post/encryption-and-decryption-in-python/
'''
import base64

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def encrypt(message, password):
    password = password.encode()
    message = message.encode()
    salt = b'salt_'
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password))
    f = Fernet(key)
    encryptedMessage = f.encrypt(message)
    return encryptedMessage


def decrypt(encryptedMessage, password):
    password = password.encode()
    encryptedMessage = encryptedMessage.encode()
    salt = b'salt_'
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password))
    f = Fernet(key)
    message = f.decrypt(encryptedMessage)
    return message.decode()
