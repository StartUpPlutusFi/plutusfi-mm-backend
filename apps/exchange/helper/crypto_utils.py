import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.exceptions import InvalidKey


class EncryptationTool:
    __salt = b'\x84\x93a\xd1\x1f\x91\xad\xfa\xb1\xb9\xe1\x14\xfb\x03`\x89J\xfb\x19\xc7\xf5I:WP2p@\x96\xd7\xac\xb3q\xdb\
    xf8\x1d\xb9\xb0\x1f\xa8J+\xccl\x82\x96\x1c\xab\xc9z\xa6L\xeb\xa6\x1e\x03X\xc5^u\xf9\'\xfa\xf5)Z*c8\xffk\xe0P\x1f\
    xf7\xf7Y}z\xaa\x02\xf5\xd9\xcd\x93w-6\xf3X\xd5S\x96\xd6\xa5\r\xa6\xae\xc4\xdc\xab\x9bK\x94\xb9N\x82\xe8\x8c\xfd_\
    x08T\\\xe1\x8e\x0c}{\x9b\x03\x1d9;\x86"\xf1c\xedb\x08\xb0\xd4\xcacO\x1f9X\x89\xfe\xcd2\xe9\x9a\x10T\xcc\x0e\xb8b%\
    xc0\x0f\x965\xc6t\xceN\x95a\xce\xf1\xcd4\xe2\xfcz\xd6\xa4bC\x84\xc39h\x97\xfaq\x9e\x15\x1e\xa1\xc8\xde\xd4\xaa\xe0\
    xe7\xb6\xd7\xb6(\xf4j\x97\xb2\x9fMf\xe4\x82\xa7/\x1e\x1c\xe1\xd0\x1c\x1b+\xd5\xe5+\xf0\x99\xd6\x8d&\x8f$H\x12\xcel\
    x94%\x02\xc4\xb6\xc3\xdc\xe7,/v\xcb\x04d\xd1\x815\xf8\x14\xe4m\x8f\x98\xfd,\xd5F)\x0b\xd2'

    __kdf = PBKDF2HMAC(
        algorithm=hashes.SHA512(),
        length=32,
        salt=__salt,
        iterations=1000000,
        backend=default_backend()
    )
    __key = base64.urlsafe_b64encode(__kdf.derive(str(os.getenv('SECRET_KEY')).encode('utf-8')))
    __f = Fernet(__key)

    @classmethod
    def encrypt(cls, text: bytes) -> str:
        token = cls.__f.encrypt(text)
        return str(token, 'utf-8')

    @classmethod
    def read(cls, text: str) -> str:
        token = text.encode('utf-8')
        return str(cls.__f.decrypt(token), 'utf-8')
