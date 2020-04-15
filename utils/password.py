import time
import datetime

import codecs
import os
from hashlib import (sha256)

from flask_bcrypt import (
    check_password_hash,
    generate_password_hash)


def hashPassword(password):
    return generate_password_hash(password, 12).decode('UTF-8')


def comparePasswords(curr, new):
    return check_password_hash(curr, new)


def parseDate(myDateTime):
    res = (datetime.datetime(myDateTime.year, myDateTime.month, myDateTime.day, myDateTime.hour,
                             myDateTime.minute, myDateTime.second) - datetime.datetime(1970, 1, 1)).total_seconds()
    return res


def changePasswordAfter(jwtTimestamp, passwordChangedAt):
    if passwordChangedAt:
        changedTime = parseDate(
            passwordChangedAt) / 1000
        return jwtTimestamp < changedTime
    # false means not changed
    return False


def cryptToken(token):
    b = bytes(token, 'utf-8')
    crypted = sha256(
    )
    crypted.update(
        b)

    return crypted.hexdigest()


def createPasswordResetToken():
    resetToken = codecs.encode(
        os.urandom(32), 'hex').decode()

    password_reset_token = cryptToken(
        resetToken)

    password_reset_expire = int(
        round(time.time() * 1000)) + 10 * 60 * 1000

    return {"rt": resetToken,
            "prt": password_reset_token,
            "pre": password_reset_expire}
