import jwt
import os
from datetime import datetime


def signToken(id):
    return jwt.encode({'id': id, 'iat': datetime.utcnow(),
                       'exp': datetime.utcnow()},
                      os.getenv(
                          'JWT_SECRET'),
                      algorithm='HS256').decode("utf-8")
