import jwt
import os
from datetime import datetime
import time


def signToken(id):
    return jwt.encode({"id": id, "iat": int(
        round(time.time() * 1000)),
        "exp": int(
        round(time.time() * 1000)) + 90*24*60*60*1000},
        os.getenv(
        'JWT_SECRET'),
        algorithm='HS256').decode("utf-8")


def checkToken(token):
    return jwt.decode(token, os.getenv('JWT_SECRET'), algorithms=['HS256'])
